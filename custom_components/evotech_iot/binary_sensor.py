from .const import DOMAIN
from .entity import EvotechEntity
from homeassistant.components.binary_sensor import BinarySensorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    defs = data["definitions"]
    entities = []
    for d in defs:
        for e in d["entities"]:
            if e["type"] == "binary_sensor":
                entities.append(EvotechBinarySensor(coordinator, d, e))
    async_add_entities(entities)

class EvotechBinarySensor(EvotechEntity, BinarySensorEntity):
    @property
    def is_on(self):
        try:
            return bool(self.coordinator.data[self.device_id].get(self.key))
        except KeyError:
            return None

    @property
    def device_class(self):
        return self.entity_def.get("device_class")
