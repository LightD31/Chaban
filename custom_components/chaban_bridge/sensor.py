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
                    results = await response.json()  # API retourne directement une liste
                    
                    # Convert dates
                    for result in results:
                        date = datetime.strptime(result['date_passage'], '%Y-%m-%d')
                        result['fermeture_a_la_circulation'] = datetime.combine(
                            date.date(),
                            datetime.strptime(result['fermeture_a_la_circulation'], '%H:%M').time()
                        )
                        result['re_ouverture_a_la_circulation'] = datetime.combine(
                            date.date(),
                            datetime.strptime(result['re_ouverture_a_la_circulation'], '%H:%M').time()
                        )

                # Get current state
                async with session.get(
                    "https://api.drndvs.fr/api/v1/chaban/state"
                ) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error getting bridge state: {response.status}")
                    state_data = await response.json()

                return {
                    "closures": results,  # Utilisation directe de la liste results
                    "current_state": state_data
                }

class ChabanBridgeSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "Chaban Bridge Next 5 Closures"

    @property
    def unique_id(self):
        return "chaban_bridge_next_5_closures"

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
                "bateau": closure["bateau"],
                "date_passage": closure["fermeture_a_la_circulation"].date().isoformat(),
                "fermeture_a_la_circulation": closure["fermeture_a_la_circulation"].isoformat(),
                "re_ouverture_a_la_circulation": closure["re_ouverture_a_la_circulation"].isoformat(),
                "type_de_fermeture": closure["type_de_fermeture"],
                "fermeture_totale": closure["fermeture_totale"],
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
