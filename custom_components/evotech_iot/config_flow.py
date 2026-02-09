"""Config flow for Evotech IoT."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_API_URL, CONF_TOKEN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_URL, default="https://evotechcar.pl/wp-json/evotech/v1"): str,
    vol.Required(CONF_TOKEN): str,
})

async def validate_input(hass: HomeAssistant, data: dict):
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    url = f"{data[CONF_API_URL]}/ha/devices"
    headers = {"Authorization": f"Bearer {data[CONF_TOKEN]}"}
    
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            raise Exception(f"Cannot connect: {resp.status}")
        json_data = await resp.json()
        if "devices" not in json_data:
            raise Exception("Invalid response format")
            
    return {"title": "Evotech Cloud"}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except Exception as e:
                _LOGGER.error("Auth error: %s", e)
                errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

