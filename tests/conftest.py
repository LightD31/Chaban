"""Test configuration for Chaban Bridge integration."""
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.chaban_bridge.const import DOMAIN


@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Return a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Pont Chaban-Delmas",
        data={"update_interval": 3600},
        unique_id="chaban_bridge",
    )


@pytest.fixture
async def mock_hass():
    """Return a mock Home Assistant instance."""
    hass = HomeAssistant()
    return hass
