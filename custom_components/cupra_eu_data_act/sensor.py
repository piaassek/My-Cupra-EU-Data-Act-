"""Sensor platform for EUDA integration."""

import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.icon import icon_for_battery_level

from .const import DOMAIN
from .coordinator import EUDADataUpdateCoordinator
from .pycupra_lib.const import EUDA_DATA_DICT

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = [
    "battery_level",
    "electric_range",
    "mileage",
    "target_soc",
    "charging_remaining_time",
    "battery_temperature_max",
    "battery_temperature_min",
    "target_climatisation_temperature",
    "climatisation_status",
    "window_heating",
    "plug_connection_state",
    "plug_lock_state",
    "service_inspection_days",
    "short_term_distance",
    "short_term_duration",
    "short_term_average_electric_engine_consumption",
    "long_term_distance",
    "long_term_duration",
    "long_term_average_electric_engine_consumption",
    "position_latitude",
    "position_longitude",
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up EUDA sensors from a config entry."""
    coordinator: EUDADataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    vehicle = coordinator.data

    entities = []
    for sensor_key in SENSOR_TYPES:
        if sensor_key in EUDA_DATA_DICT:
            sensor_def = EUDA_DATA_DICT[sensor_key]
            entities.append(EUDASensor(coordinator, vehicle, sensor_key, sensor_def))

    # Add extra sensor for last update timestamp
    entities.append(EUDALastUpdateSensor(coordinator, vehicle))

    async_add_entities(entities)


class EUDASensor(CoordinatorEntity[EUDADataUpdateCoordinator], SensorEntity):
    """Representation of an EUDA Sensor."""

    def __init__(
        self,
        coordinator: EUDADataUpdateCoordinator,
        vehicle,
        sensor_key: str,
        sensor_def: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._sensor_def = sensor_def
        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_key
        self._vin = coordinator.vin
        self._attr_unique_id = f"{self._vin}-euda-sensor-{sensor_key}"
        self._attr_native_unit_of_measurement = sensor_def.get("unit")
        
        dev_class = sensor_def.get("device_class")
        if dev_class:
            self._attr_device_class = dev_class

        if sensor_key in [
            "battery_level",
            "electric_range",
            "mileage",
            "battery_temperature_max",
            "battery_temperature_min",
            "target_climatisation_temperature",
            "short_term_distance",
            "short_term_duration",
            "short_term_average_electric_engine_consumption",
            "long_term_distance",
            "long_term_duration",
            "long_term_average_electric_engine_consumption",
        ]:
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def vehicle(self):
        """Return the vehicle object."""
        return self.coordinator.data

    @property
    def native_value(self):
        """Return native sensor value."""
        if not self.vehicle:
            return None
        key = self._sensor_def.get("key")
        keys = self._sensor_def.get("keys", [key] if key else [])
        field_names = self._sensor_def.get("field_names", [])
        conversion = self._sensor_def.get("conversion")
        return self.vehicle.getEUDADataFieldValue(keys, conversion, field_names=field_names)

    @property
    def icon(self) -> Optional[str]:
        """Return dynamic icon."""
        if self._sensor_key == "battery_level":
            val = self.native_value
            if val is not None:
                try:
                    return icon_for_battery_level(battery_level=int(val))
                except Exception:
                    pass
        return self._sensor_def.get("icon")

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


class EUDALastUpdateSensor(CoordinatorEntity[EUDADataUpdateCoordinator], SensorEntity):
    """Sensor showing timestamp of the newest processed EUDA data package."""

    def __init__(self, coordinator: EUDADataUpdateCoordinator, vehicle) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._vin = coordinator.vin
        self._attr_has_entity_name = True
        self._attr_translation_key = "last_update"
        self._attr_unique_id = f"{self._vin}-euda-sensor-last_update"
        self._attr_icon = "mdi:clock-check-outline"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def native_value(self) -> Optional[datetime]:
        """Return timestamp as timezone-aware datetime or None."""
        if not self.coordinator.data:
            return None
        try:
            ts = getattr(self.coordinator.data, "getEUDAFileTimestamp", None)
            if not ts:
                return None
            if isinstance(ts, datetime):
                if ts.year <= 1 or ts == datetime.min:
                    return None
                if ts.tzinfo is None:
                    return ts.replace(tzinfo=timezone.utc)
                return ts
            if isinstance(ts, str):
                ts_str = ts.strip()
                if not ts_str or ts_str in ["unknown", "0001-01-01 00:00:00", "0001-01-01T00:00:00"]:
                    return None
                try:
                    parsed = datetime.fromisoformat(ts_str)
                    if parsed.year <= 1:
                        return None
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    return parsed
                except Exception:
                    pass
                for fmt in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y%m%d%H%M%S"):
                    try:
                        parsed = datetime.strptime(ts_str, fmt)
                        if parsed.year <= 1:
                            return None
                        if parsed.tzinfo is None:
                            parsed = parsed.replace(tzinfo=timezone.utc)
                        return parsed
                    except Exception:
                        pass
        except Exception as err:
            _LOGGER.debug(f"Error parsing last update timestamp: {err}")
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information."""
        veh = self.coordinator.data
        return DeviceInfo(
            identifiers={(DOMAIN, self._vin)},
            name=veh.nickname if veh and veh.nickname else self._vin,
            manufacturer=veh.brand.title() if veh and veh.brand else "Cupra",
            model=veh.model.title() if veh and veh.model else "Born",
            serial_number=self._vin,
        )
