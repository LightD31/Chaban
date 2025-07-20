"""Support for Chaban Bridge sensor."""
from __future__ import annotations

import asyncio
import aiohttp
import async_timeout
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
    CoordinatorEntity,
)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN, 
    CONF_UPDATE_INTERVAL, 
    DEFAULT_UPDATE_INTERVAL,
    API_CLOSURES_URL,
    API_STATE_URL,
    MANUFACTURER,
    MODEL,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Chaban Bridge sensor from a config entry."""
    update_interval = timedelta(
        seconds=config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    )

    coordinator = ChabanBridgeDataUpdateCoordinator(hass, update_interval)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([ChabanBridgeSensor(coordinator, config_entry)], True)

class ChabanBridgeDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""
    
    def __init__(self, hass: HomeAssistant, update_interval: timedelta) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Chaban Bridge",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    # Get planned closures
                    async with session.get(
                        f"{API_CLOSURES_URL}?limit=5"
                    ) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error communicating with API: {response.status}")
                        results = await response.json()
                        
                        # Convert dates
                        for result in results:
                            result['start_date'] = datetime.fromisoformat(result['start_date'])
                            result['end_date'] = datetime.fromisoformat(result['end_date'])

                    # Get current state
                    async with session.get(API_STATE_URL) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error getting bridge state: {response.status}")
                        state_data = await response.json()

                    return {
                        "closures": results,
                        "current_state": state_data
                    }
        except asyncio.TimeoutError as exc:
            raise UpdateFailed("Timeout communicating with API") from exc
        except aiohttp.ClientError as exc:
            raise UpdateFailed(f"Error communicating with API: {exc}") from exc

class ChabanBridgeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Chaban Bridge sensor."""
    
    def __init__(self, coordinator: ChabanBridgeDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = "chaban_bridge"
        self._attr_name = "Pont Chaban Delmas"
        self._attr_icon = "mdi:bridge"
        self._attr_device_class = SensorDeviceClass.ENUM

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this sensor."""
        return DeviceInfo(
            identifiers={(DOMAIN, "chaban_bridge")},
            name="Pont Chaban-Delmas",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="1.0",
            configuration_url="https://github.com/lightd31/Chaban",
        )

    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data["current_state"]["state"]

    @property
    def icon(self) -> str:
        """Return the icon for the sensor."""
        if not self.coordinator.data:
            return "mdi:bridge"
        
        is_closed = self.coordinator.data["current_state"].get("is_closed", False)
        return "mdi:bridge-off" if is_closed else "mdi:bridge"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
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
