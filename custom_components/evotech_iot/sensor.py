from .const import DOMAIN
from .entity import EvotechEntity
from homeassistant.components.sensor import SensorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    defs = data["definitions"]
    
    entities = []
    for d in defs:
        for e in d["entities"]:
            if e["type"] == "sensor":
                entities.append(EvotechSensor(coordinator, d, e))
    async_add_entities(entities)

class EvotechSensor(EvotechEntity, SensorEntity):
    @property
    def native_value(self):
        try:
            return self.coordinator.data[self.device_id].get(self.key)
        except KeyError:
            return None

    @property
    def native_unit_of_measurement(self):
        return self.entity_def.get("unit")

    @property
    def device_class(self):
        return self.entity_def.get("device_class")

    @property
    def icon(self):
        return self.entity_def.get("icon")
