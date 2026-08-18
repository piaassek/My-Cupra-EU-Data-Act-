"""Coordinator for EUDA (EU Data Act) integration."""

import asyncio
from datetime import timedelta
import logging
from typing import Dict, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

from .const import DOMAIN, CONF_BRAND, CONF_VEHICLE, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .pycupra_lib.eudaconnection import EUDAConnection
from .pycupra_lib.eudavehicle import EUDAVehicle

_LOGGER = logging.getLogger(__name__)


class EUDADataUpdateCoordinator(DataUpdateCoordinator[EUDAVehicle]):
    """Class to manage fetching EUDA telemetry data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.hass = hass
        self.vin = entry.data.get(CONF_VEHICLE, "").upper()
        self.brand = entry.data.get(CONF_BRAND, "cupra")
        self.username = entry.data.get(CONF_USERNAME, "")
        self.password = entry.data.get(CONF_PASSWORD, "")

        scan_interval_min = entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        update_interval = timedelta(minutes=max(1, scan_interval_min))

        self.session = async_create_clientsession(hass)
        self.connection = EUDAConnection(
            session=self.session,
            brand=self.brand,
            username=self.username,
            password=self.password,
            fulldebug=False,
            hass=hass,
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.vin}",
            update_interval=update_interval,
        )

    async def async_login(self) -> bool:
        """Perform login to EUDA portal."""
        _LOGGER.info(f"Logging in to EUDA portal ({self.brand}) for {self.username}...")
        success = await self.connection.doLogin()
        if not success:
            _LOGGER.error(f"Failed to log in to EUDA portal for {self.username}.")
            return False
        
        await self.connection.getVehicles()
        _LOGGER.info(f"EUDA vehicles found: {[v.vin for v in self.connection.vehicles]}")
        return True

    async def _async_update_data(self) -> EUDAVehicle:
        """Fetch latest vehicle data from EUDA."""
        _LOGGER.debug(f"Fetching EUDA telemetry update for VIN: {self.vin}")
        try:
            success = await self.connection.update()
            vehicle = self.connection.vehicle(self.vin)
            if vehicle is None:
                if len(self.connection.vehicles) > 0:
                    vehicle = self.connection.vehicles[0]
                else:
                    raise UpdateFailed(f"No EUDA vehicle found matching VIN {self.vin}")
            
            _LOGGER.info(f"EUDA update successful for {self.vin}. (Battery: {vehicle.battery_level}%, Range: {vehicle.electric_range}km)")
            return vehicle
        except Exception as err:
            _LOGGER.error(f"Error fetching EUDA data: {err}")
            raise UpdateFailed(f"Error communicating with EUDA API: {err}") from err
