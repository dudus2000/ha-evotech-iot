from .const import DOMAIN
from .entity import EvotechEntity
from homeassistant.components.switch import SwitchEntity
import logging

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    defs = data["definitions"]
    entities = []
    for d in defs:
        for e in d["entities"]:
            if e["type"] == "switch":
                entities.append(EvotechSwitch(coordinator, d, e))
    async_add_entities(entities)

class EvotechSwitch(EvotechEntity, SwitchEntity):
    @property
    def is_on(self):
        try:
            return bool(self.coordinator.data[self.device_id].get(self.key))
        except KeyError:
            return False

    async def async_turn_on(self, **kwargs):
        await self.coordinator.send_command(self.device_id, self.key, "ON")

    async def async_turn_off(self, **kwargs):
        await self.coordinator.send_command(self.device_id, self.key, "OFF")
