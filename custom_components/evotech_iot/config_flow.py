"""Config flow for Evotech IoT."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_API_URL, CONF_TOKEN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_URL, default="https://twojastrona.pl/wp-json/evotech/v1"): str,
    vol.Required(CONF_TOKEN): str,
})

async def validate_input(hass: HomeAssistant, data: dict):
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api_url = data[CONF_API_URL].rstrip("/")
    url = f"{api_url}/ha/devices?token={data[CONF_TOKEN]}"
    headers = {"Authorization": f"Bearer {data[CONF_TOKEN]}"}
    
    _LOGGER.error("DEBUG CONNECTING TO: %s", url)
    
    async with session.get(url, headers=headers, ssl=False) as resp:
        if resp.status != 200:
            _LOGGER.error("Connect failed with status: %s", resp.status)
            raise Exception(f"Cannot connect: {resp.status}")
        text = await resp.text()
        _LOGGER.error("DEBUG RAW TEXT: %r", text[:200]) # Log first 200 chars

        # Aggressive cleanup: find first {
        idx = text.find("{")
        if idx != -1:
            text = text[idx:]
        
        _LOGGER.error("DEBUG CLEANED TEXT: %r", text[:200]) # Log cleaned text

        import json
        try:
            json_data = json.loads(text)
        except Exception as e:
            _LOGGER.error("JSON decode failed: %s. Content: %s", e, text[:200])
            raise
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
