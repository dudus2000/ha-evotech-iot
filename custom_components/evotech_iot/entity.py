from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

class EvotechEntity(CoordinatorEntity):
    """Base entity."""
    def __init__(self, coordinator, device_def, entity_def):
        super().__init__(coordinator)
        self.device_def = device_def
        self.entity_def = entity_def
        self.device_id = device_def["id"]
        self.key = entity_def["key"]
        
    @property
    def unique_id(self):
        return f"{self.device_id}_{self.key}"

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self.device_id)},
            name=self.device_def["name"],
            model=self.device_def.get("model"),
            sw_version=self.device_def.get("sw_version"),
            manufacturer="Krystian Car",
        )

    @property
    def name(self):
        return f"{self.device_def['name']} {self.entity_def['name']}"
        
    @property
    def available(self):
        # Sprawdzamy czy mamy dane dla tego urządzenia
        return self.coordinator.data and self.device_id in self.coordinator.data
