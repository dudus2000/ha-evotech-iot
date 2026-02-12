"""The Evotech IoT integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS, CONF_API_URL, CONF_TOKEN
from .coordinator import EvotechCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Evotech IoT from a config entry."""
    api_url = entry.data[CONF_API_URL]
    token = entry.data[CONF_TOKEN]

    # 1. Fetch devices definitions (once)
    session = async_get_clientsession(hass)
    device_def_url = f"{api_url}/ha/devices?token={token}"
    
    try:
        async with session.get(device_def_url, headers={"Authorization": f"Bearer {token}"}) as resp:
            if resp.status != 200:
                return False
            text = await resp.text()
            _LOGGER.error("DEBUG INIT RAW: %r", text[:500]) # Log first 500 chars

            # Aggressive cleanup
            idx = text.find("{")
            if idx != -1: text = text[idx:]
            
            import json
            data = json.loads(text)
            devices_definitions = data.get("devices", [])
    except Exception as e:
        _LOGGER.error("Failed to fetch definitions: %s", e)
        return False

    # 2. Setup Coordinator
    coordinator = EvotechCoordinator(hass, api_url, token)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "definitions": devices_definitions
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
