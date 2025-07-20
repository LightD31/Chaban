"""Constants for the Chaban Bridge integration."""

DOMAIN = "chaban_bridge"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 300

# API URLs
API_BASE_URL = "https://api.drndvs.fr/api/v1/chaban"
API_CLOSURES_URL = f"{API_BASE_URL}/closures"
API_STATE_URL = f"{API_BASE_URL}/state"

# Device information
MANUFACTURER = "Bordeaux Métropole"
MODEL = "Bridge Sensor"
