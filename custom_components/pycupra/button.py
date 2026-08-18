"""Button platform for EUDA integration."""

import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EUDADataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up EUDA button platform."""
    coordinator: EUDADataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    vehicle = coordinator.data

    async_add_entities([EUDARefreshButton(coordinator, vehicle)])


class EUDARefreshButton(CoordinatorEntity[EUDADataUpdateCoordinator], ButtonEntity):
    """Representation of an EUDA Refresh Button."""

    def __init__(self, coordinator: EUDADataUpdateCoordinator, vehicle) -> None:
        """Initialize button."""
        super().__init__(coordinator)
        self._vin = coordinator.vin
        self._attr_name = f"{vehicle.nickname or self._vin} Request Update"
        self._attr_unique_id = f"{self._vin}-euda-button-refresh"
        self._attr_icon = "mdi:cloud-download"

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info(f"Manual EUDA refresh requested for {self._vin}")
        await self.coordinator.async_request_refresh()

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
