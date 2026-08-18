"""Binary sensor platform for EUDA integration."""

import logging
from typing import Optional, Dict, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EUDADataUpdateCoordinator
from .pycupra_lib.const import EUDA_DATA_DICT

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_TYPES = {
    "is_parked": {
        "name": "Is Parked",
        "icon": "mdi:car-parking-lights",
        "key": "37af0223-6d24-3ba0-9ce9-f1701d247961",
        "field_names": ["is_parked", "parking_light_left", "parking_light_right"],
        "type": "bool",
    },
    "is_connected": {
        "name": "Is Online",
        "device_class": BinarySensorDeviceClass.CONNECTIVITY,
        "key": "4cbef03f-a75b-3fe9-a22f-f3fbbe8dd003",
        "field_names": ["is_connected", "state"],
        "type": "bool",
    },
    "locked": {
        "name": "Locked",
        "device_class": BinarySensorDeviceClass.LOCK,
        "key": "bd917b58-82bd-3c34-a006-747ca5aec03d",
        "field_names": ["locked", "lock_state"],
        "type": "bool",
    },
    "mirror_heating": {
        "name": "Mirror Heating Enabled",
        "icon": "mdi:car-side",
        "key": "6b01af98-9b04-38cb-a2a6-3120cce7a162",
        "field_names": ["mirror_heating_state", "mirror_heating"],
        "type": "bool",
    },
    "trunk_lid_status": {
        "name": "Trunk",
        "device_class": BinarySensorDeviceClass.DOOR,
        "key": "c1a779dc-6dc7-38dd-8f46-a5ddf0d2c5f5",
        "field_names": ["decklid_status", "trunk_lid_status", "trunk_status"],
        "type": "open_closed",
    },
    "hood_status": {
        "name": "Hood",
        "device_class": BinarySensorDeviceClass.OPENING,
        "key": "e4c66263-aa68-3afc-9b9f-af7146c83277",
        "field_names": ["hood_status", "bonnet_status"],
        "type": "open_closed",
    },
    "window_front_left": {
        "name": "Window Front Left",
        "device_class": BinarySensorDeviceClass.WINDOW,
        "key": "63bbeb15-1b73-3b7f-8c0a-6fac6851f98b",
        "field_names": ["window_front_left", "window_lift_front_left_status"],
        "type": "open_closed",
    },
    "window_front_right": {
        "name": "Window Front Right",
        "device_class": BinarySensorDeviceClass.WINDOW,
        "key": "8733f7cc-f191-384b-8805-0ecbdb5ff45f",
        "field_names": ["window_front_right", "window_lift_front_right_status"],
        "type": "open_closed",
    },
    "window_rear_left": {
        "name": "Window Rear Left",
        "device_class": BinarySensorDeviceClass.WINDOW,
        "key": "d4e79704-e8a0-3e30-a865-5e44ca1d316f",
        "field_names": ["window_rear_left", "window_lift_rear_left_status"],
        "type": "open_closed",
    },
    "window_rear_right": {
        "name": "Window Rear Right",
        "device_class": BinarySensorDeviceClass.WINDOW,
        "key": "b95233db-0a75-3846-ba7c-1db17df235f6",
        "field_names": ["window_rear_right", "window_lift_rear_right_status"],
        "type": "open_closed",
    },
    "plug_connected": {
        "name": "Cable Connected",
        "device_class": BinarySensorDeviceClass.PLUG,
        "key": "17e75411-e651-3ba5-9358-6aab3b022581",
        "field_names": ["plug_state", "charging_plug1_connectionstate", "plug_connection_state"],
        "type": "plug_state",
    },
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up EUDA binary sensors from a config entry."""
    coordinator: EUDADataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    vehicle = coordinator.data

    entities = [
        EUDABinarySensor(coordinator, vehicle, sensor_key, sensor_def)
        for sensor_key, sensor_def in BINARY_SENSOR_TYPES.items()
    ]

    async_add_entities(entities)


class EUDABinarySensor(CoordinatorEntity[EUDADataUpdateCoordinator], BinarySensorEntity):
    """Representation of an EUDA Binary Sensor."""

    def __init__(
        self,
        coordinator: EUDADataUpdateCoordinator,
        vehicle,
        sensor_key: str,
        sensor_def: Dict[str, Any],
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._sensor_def = sensor_def
        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_key
        self._attr_name = sensor_def.get("name", sensor_key.title())
        self._vin = coordinator.vin
        self._attr_unique_id = f"{self._vin}-euda-binary_sensor-{sensor_key}"
        
        if "device_class" in sensor_def:
            self._attr_device_class = sensor_def["device_class"]
        if "icon" in sensor_def:
            self._attr_icon = sensor_def["icon"]

    @property
    def vehicle(self):
        """Return the vehicle object."""
        return self.coordinator.data

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if binary sensor is on."""
        if not self.vehicle:
            return None

        key = self._sensor_def.get("key")
        keys = self._sensor_def.get("keys", [key] if key else [])
        field_names = self._sensor_def.get("field_names", [])
        st_type = self._sensor_def.get("type")

        val = self.vehicle.getEUDADataFieldValue(keys, field_names=field_names)

        if val is None or val == "":
            return None

        if st_type == "bool":
            return str(val).lower() in ("true", "on", "valid", "1")
        elif st_type == "open_closed":
            return str(val).upper() in ["OPEN", "UNLOCKED", "TRUE", "1"]
        elif st_type == "plug_state":
            return str(val).upper() in ["CONNECTED", "PLUGGED", "TRUE", "1"]

        return bool(val)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._vin)},
            name=self.vehicle.nickname or self._vin,
            manufacturer=self.vehicle.brand.title() if self.vehicle.brand else "Cupra",
            model=self.vehicle.model.title() if self.vehicle.model else "Born",
            serial_number=self._vin,
        )
