"""Device tracker platform for EUDA integration."""

import logging
from typing import Optional

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EUDADataUpdateCoordinator
from .pycupra_lib.const import (
    EUDA_DATA_CONVERSION_FLOAT,
)

_LOGGER = logging.getLogger(__name__)

LATITUDE_KEY = "ec0ab527-361b-3ada-820e-99f601f69d7b"
LONGITUDE_KEY = "61be015f-17b5-3b59-9c61-e3c66199514e"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up EUDA device tracker."""
    coordinator: EUDADataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    vehicle = coordinator.data

    async_add_entities([EUDADeviceTracker(coordinator, vehicle)])


class EUDADeviceTracker(CoordinatorEntity[EUDADataUpdateCoordinator], TrackerEntity):
    """Representation of an EUDA GPS Tracker."""

    def __init__(self, coordinator: EUDADataUpdateCoordinator, vehicle) -> None:
        """Initialize tracker."""
        super().__init__(coordinator)
        self._vin = coordinator.vin
        self._attr_has_entity_name = True
        self._attr_translation_key = "location"
        self._attr_unique_id = f"{self._vin}-euda-tracker"
        self._attr_icon = "mdi:car"

    @property
    def vehicle(self):
        """Return vehicle."""
        return self.coordinator.data

    @property
    def latitude(self) -> Optional[float]:
        """Return latitude value of the device."""
        if not self.vehicle:
            return None
        val = self.vehicle.getEUDADataFieldValue(LATITUDE_KEY, EUDA_DATA_CONVERSION_FLOAT)
        return float(val) if val is not None else None

    @property
    def longitude(self) -> Optional[float]:
        """Return longitude value of the device."""
        if not self.vehicle:
            return None
        val = self.vehicle.getEUDADataFieldValue(LONGITUDE_KEY, EUDA_DATA_CONVERSION_FLOAT)
        return float(val) if val is not None else None

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

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
