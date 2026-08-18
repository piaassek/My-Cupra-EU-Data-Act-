"""Config flow for EUDA (EU Data Act) integration."""

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_BRAND,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_VEHICLE,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    BRANDS,
)
from .pycupra_lib.eudaconnection import EUDAConnection

_LOGGER = logging.getLogger(__name__)


class EUDAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EUDA integration."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._brand: str = "cupra"
        self._username: str = ""
        self._password: str = ""
        self._vehicles: list = []
        self._errors: dict = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial user step (credentials)."""
        self._errors = {}

        if user_input is not None:
            self._brand = user_input[CONF_BRAND].lower()
            self._username = user_input[CONF_USERNAME].strip()
            self._password = user_input[CONF_PASSWORD]

            # Validate credentials against EUDA portal
            session = async_create_clientsession(self.hass)
            connection = EUDAConnection(
                session=session,
                brand=self._brand,
                username=self._username,
                password=self._password,
                hass=self.hass,
            )

            try:
                success = await connection.doLogin()
                if not success:
                    self._errors["base"] = "invalid_auth"
                else:
                    await connection.getVehicles()
                    self._vehicles = connection.vehicles

                    if not self._vehicles:
                        self._errors["base"] = "no_vehicles"
                    elif len(self._vehicles) == 1:
                        # Auto-select single vehicle
                        vin = self._vehicles[0].vin
                        name = self._vehicles[0].nickname or vin
                        await self.async_set_unique_id(vin)
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=f"{self._brand.title()} ({name})",
                            data={
                                CONF_BRAND: self._brand,
                                CONF_USERNAME: self._username,
                                CONF_PASSWORD: self._password,
                                CONF_VEHICLE: vin,
                                CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                            },
                        )
                    else:
                        # Multiple vehicles found, let user pick
                        return await self.async_step_vehicle()
            except config_entries.FlowResult as fr:
                raise fr
            except Exception as err:
                # Check if it's an AbortFlow or other HA flow exception
                if err.__class__.__name__ == "AbortFlow":
                    raise err
                _LOGGER.error(f"Login error during config flow: {err}")
                self._errors["base"] = "cannot_connect"
            finally:
                await connection.terminate()

        schema = vol.Schema(
            {
                vol.Required(CONF_BRAND, default="cupra"): vol.In(BRANDS),
                vol.Required(CONF_USERNAME, default=self._username): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=self._errors,
        )

    async def async_step_vehicle(self, user_input=None):
        """Handle vehicle selection step for multiple vehicles."""
        self._errors = {}

        if user_input is not None:
            vin = user_input[CONF_VEHICLE]
            scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            
            # Find chosen vehicle
            veh = next((v for v in self._vehicles if v.vin == vin), None)
            name = veh.nickname if veh and veh.nickname else vin

            await self.async_set_unique_id(vin)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"{self._brand.title()} ({name})",
                data={
                    CONF_BRAND: self._brand,
                    CONF_USERNAME: self._username,
                    CONF_PASSWORD: self._password,
                    CONF_VEHICLE: vin,
                    CONF_SCAN_INTERVAL: scan_interval,
                },
            )

        vehicle_dict = {
            v.vin: f"{v.nickname} ({v.vin})" if v.nickname else v.vin
            for v in self._vehicles
        }

        schema = vol.Schema(
            {
                vol.Required(CONF_VEHICLE): vol.In(vehicle_dict),
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                    vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=1440)
                ),
            }
        )

        return self.async_show_form(
            step_id="vehicle",
            data_schema=schema,
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return EUDAOptionsFlowHandler(config_entry)


class EUDAOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle EUDA options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=current_interval): vol.All(
                    vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=1440)
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
