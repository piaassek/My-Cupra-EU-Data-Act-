"""Constants for the EUDA Cupra / VW Group integration."""

from homeassistant.const import Platform

DOMAIN = "cupra_eu_data_act"

CONF_BRAND = "brand"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_VEHICLE = "vehicle"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 15  # minutes
MIN_SCAN_INTERVAL = 5  # minutes

BRANDS = [
    "cupra",
    "volkswagen",
    "skoda",
    "seat",
    "audi",
]

PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.BUTTON,
]
