"""EUDA (EU Data Act) Integration for Home Assistant."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .coordinator import EUDADataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the EUDA PyCupra component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EUDA PyCupra from a config entry."""
    _LOGGER.info(f"Setting up EUDA integration for {entry.title}...")

    coordinator = EUDADataUpdateCoordinator(hass, entry)

    # Perform initial login and vehicle discovery
    try:
        logged_in = await coordinator.async_login()
        if not logged_in:
            raise ConfigEntryNotReady(f"Could not login to EUDA portal for {coordinator.username}")
    except Exception as err:
        _LOGGER.error(f"Failed to connect to EUDA during setup: {err}")
        raise ConfigEntryNotReady(f"Failed to connect to EUDA: {err}") from err

    # Perform first data refresh
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Forward setup to all platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Add options update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    _LOGGER.info(f"EUDA integration setup completed successfully for {entry.title}.")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info(f"Unloading EUDA integration for {entry.title}...")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
        if coordinator and coordinator.connection:
            try:
                await coordinator.connection.terminate()
            except Exception as e:
                _LOGGER.debug(f"Error terminating connection: {e}")

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
