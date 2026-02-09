"""Constants for the Evotech IoT integration."""
from datetime import timedelta

DOMAIN = "evotech_iot"
CONF_API_URL = "api_url"
CONF_TOKEN = "token"

# Jak często HA ma pytać API o stany (w sekundach)
SCAN_INTERVAL = timedelta(seconds=10)

PLATFORMS = ["sensor", "binary_sensor", "switch", "device_tracker"]
