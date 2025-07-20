"""Support for Chaban Bridge sensor."""
from __future__ import annotations

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
                        closures_data = await response.json()

                        # Convert dates for each closure
                        for closure in closures_data.get("closures", []):
                            closure['start_date'] = datetime.fromisoformat(closure['start_date'])
                            closure['end_date'] = datetime.fromisoformat(closure['end_date'])

                    # Get current state
                    async with session.get(API_STATE_URL) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error getting bridge state: {response.status}")
                        state_data = await response.json()

                    return {
                        "closures": closures_data.get("closures", []),
                        "count": closures_data.get("count", 0),
                        "current_state": state_data
                    }
        except TimeoutError as exc:
            raise UpdateFailed("Timeout communicating with API") from exc
        except aiohttp.ClientError as exc:
            raise UpdateFailed(f"Error communicating with API: {exc}") from exc

class ChabanBridgeSensor(SensorEntity):
    """Representation of a Chaban Bridge sensor."""

    def __init__(self, coordinator: ChabanBridgeDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._config_entry = config_entry
        self._attr_unique_id = "chaban_bridge"
        self._attr_name = "Pont Chaban Delmas"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_should_poll = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "chaban_bridge")},
            name="Pont Chaban-Delmas",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="1.0",
            configuration_url="https://github.com/lightd31/Chaban",
        )
        # Initialize attributes with default values
        self._attr_native_value = None
        self._attr_icon = "mdi:bridge"
        self._attr_extra_state_attributes = {}
        self._attr_available = True

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    async def async_update(self) -> None:
        """Update the entity. Only used by the generic entity update service."""
        await self.coordinator.async_request_refresh()

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Update availability based on coordinator success
        self._attr_available = self.coordinator.last_update_success

        if not self.coordinator.data:
            self._attr_native_value = None
            self._attr_icon = "mdi:bridge"
            self._attr_extra_state_attributes = {}
        else:
            # Update native value
            self._attr_native_value = self.coordinator.data["current_state"]["state"]

            # Update icon based on bridge state
            is_closed = self.coordinator.data["current_state"].get("is_closed", False)
            self._attr_icon = "mdi:bridge-off" if is_closed else "mdi:bridge"

            # Update extra state attributes
            closures = []
            for closure in self.coordinator.data["closures"][:5]:
                closures.append({
                    "reason": closure["reason"],
                    "start_date": closure["start_date"].isoformat(),
                    "end_date": closure["end_date"].isoformat(),
                    "closure_type": closure["closure_type"],
                    "duration_minutes": closure.get("duration_minutes"),
                })

            self._attr_extra_state_attributes = {
                "current_state": self.coordinator.data["current_state"],
                "is_closed": self.coordinator.data["current_state"]["is_closed"],
                "last_update": self.coordinator.data["current_state"]["last_update"],
                "bridge_name": self.coordinator.data["current_state"]["name"],
                "closures_count": self.coordinator.data.get("count", 0),
                "closures": closures
            }

        self.async_write_ha_state()
