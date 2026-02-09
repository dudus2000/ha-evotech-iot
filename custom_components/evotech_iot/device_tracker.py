from .const import DOMAIN
from .entity import EvotechEntity
from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    defs = data["definitions"]
    entities = []
    for d in defs:
        for e in d["entities"]:
            if e["type"] == "device_tracker":
                entities.append(EvotechTracker(coordinator, d, e))
    async_add_entities(entities)

class EvotechTracker(EvotechEntity, TrackerEntity):
    @property
    def source_type(self):
        return SourceType.GPS

    @property
    def latitude(self):
        try:
            data = self.coordinator.data[self.device_id].get(self.key)
            return data.get("latitude") if data else None
        except: return None

    @property
    def longitude(self):
        try:
            data = self.coordinator.data[self.device_id].get(self.key)
            return data.get("longitude") if data else None
        except: return None
