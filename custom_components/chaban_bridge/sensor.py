import asyncio
import aiohttp
import async_timeout
from datetime import datetime, timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    update_interval = timedelta(
        seconds=config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    )

    coordinator = ChabanBridgeDataUpdateCoordinator(hass, update_interval)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([ChabanBridgeSensor(coordinator)], True)

class ChabanBridgeDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, update_interval):
        super().__init__(
            hass,
            _LOGGER,
            name="Chaban Bridge",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        async with async_timeout.timeout(10):
            async with aiohttp.ClientSession() as session:
                # Get planned closures
                async with session.get(
                    "https://api.drndvs.fr/api/v1/chaban/nextclosure?limit=5"
                ) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error communicating with API: {response.status}")
                    results = await response.json()
                    
                    # Convert dates
                    for result in results:
                        result['start_date'] = datetime.fromisoformat(result['start_date'])
                        result['end_date'] = datetime.fromisoformat(result['end_date'])

                # Get current state
                async with session.get(
                    "https://api.drndvs.fr/api/v1/chaban/state"
                ) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error getting bridge state: {response.status}")
                    state_data = await response.json()

                return {
                    "closures": results,
                    "current_state": state_data
                }

class ChabanBridgeSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "Pont Chaban Delmas"

    @property
    def unique_id(self):
        return "chaban_bridge"

    @property
    def state(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data["current_state"]["state"]

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        
        closures = []
        for closure in self.coordinator.data["closures"][:5]:
            closures.append({
                "reason": closure["reason"],
                "date": closure["start_date"].date().isoformat(),
                "start_date": closure["start_date"].isoformat(),
                "end_date": closure["end_date"].isoformat(),
                "closure_type": closure["closure_type"],
            })

        return {
            "current_state": self.coordinator.data["current_state"],
            "is_closed": self.coordinator.data["current_state"]["is_closed"],
            "last_update": self.coordinator.data["current_state"]["last_update"],
            "closures": closures
        }

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
