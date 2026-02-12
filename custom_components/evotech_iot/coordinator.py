"""DataUpdateCoordinator for Evotech IoT."""
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class EvotechCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Evotech IoT data."""

    def __init__(self, hass, api_url, token):
        self.api_url = api_url
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        self.session = async_get_clientsession(hass)

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            url = f"{self.api_url}/ha/states?token={self.token}"
            async with self.session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"Error communicating with API: {resp.status}")
                text = await resp.text()
                # Aggressive cleanup
                idx = text.find("{")
                if idx != -1: text = text[idx:]
                import json
                return json.loads(text)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def send_command(self, device_id, entity_key, state):
        """Send command to API."""
        url = f"{self.api_url}/ha/control?token={self.token}"
        payload = {
            "device_id": device_id,
            "entity_key": entity_key,
            "state": state
        }
        async with self.session.post(url, json=payload, headers=self.headers) as resp:
            if resp.status != 200:
                _LOGGER.error("Command failed: %s", await resp.text())
                return False
            # Force refresh to update UI immediately
            await self.async_request_refresh()
            return True
