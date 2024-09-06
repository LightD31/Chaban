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
                async with session.get(
                    "https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/previsions_pont_chaban/records",
                    params={
                        "where": f"date_passage >= '{datetime.now().strftime('%Y-%m-%d')}'",
                        "limit": 5,
                    },
                ) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error communicating with API: {response.status}")
                    data = await response.json()
                    results = data.get("results", [])
                    
                    # Convert string dates and times to datetime objects
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
                    
                    return results

class ChabanBridgeSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "Chaban Bridge Next Closure"

    @property
    def unique_id(self):
        return "chaban_bridge_next_closure"

    @property
    def state(self):
        if not self.coordinator.data:
            return None
        next_closure = self.coordinator.data[0]
        return next_closure['fermeture_a_la_circulation'].isoformat()

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        next_closure = self.coordinator.data[0]
        return {
            "bateau": next_closure["bateau"],
            "date_passage": next_closure["fermeture_a_la_circulation"].date().isoformat(),
            "fermeture_a_la_circulation": next_closure["fermeture_a_la_circulation"].isoformat(),
            "re_ouverture_a_la_circulation": next_closure["re_ouverture_a_la_circulation"].isoformat(),
            "type_de_fermeture": next_closure["type_de_fermeture"],
            "fermeture_totale": next_closure["fermeture_totale"],
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