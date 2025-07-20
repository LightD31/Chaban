"""Test the Chaban Bridge sensor."""
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.chaban_bridge.sensor import (
    ChabanBridgeDataUpdateCoordinator,
    ChabanBridgeSensor,
)
from custom_components.chaban_bridge.const import DOMAIN


@pytest.fixture
def coordinator(hass):
    """Return a test coordinator."""
    return ChabanBridgeDataUpdateCoordinator(hass, timedelta(seconds=3600))


@pytest.fixture
def sensor(coordinator, mock_config_entry):
    """Return a test sensor."""
    return ChabanBridgeSensor(coordinator, mock_config_entry)


@pytest.fixture
def mock_api_data():
    """Return mock API data."""
    return {
        "closures": [
            {
                "reason": "Test closure",
                "start_date": datetime.now(),
                "end_date": datetime.now() + timedelta(hours=2),
                "closure_type": "planned"
            }
        ],
        "current_state": {
            "state": "open",
            "is_closed": False,
            "last_update": datetime.now().isoformat()
        }
    }


async def test_coordinator_update_success(coordinator, mock_api_data):
    """Test successful data update."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock()
        
        # Mock the closures response
        closure_data = [{
            "reason": "Test closure",
            "start_date": "2024-01-01T10:00:00",
            "end_date": "2024-01-01T12:00:00",
            "closure_type": "planned"
        }]
        
        # Mock the state response
        state_data = {
            "state": "open",
            "is_closed": False,
            "last_update": "2024-01-01T09:00:00"
        }
        
        mock_response.json.side_effect = [closure_data, state_data]
        mock_get.return_value.__aenter__.return_value = mock_response
        
        result = await coordinator._async_update_data()
        
        assert result["closures"] == closure_data
        assert result["current_state"] == state_data


async def test_coordinator_update_api_error(coordinator):
    """Test API error handling."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_get.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()


async def test_coordinator_update_timeout(coordinator):
    """Test timeout handling."""
    with patch('aiohttp.ClientSession.get', side_effect=aiohttp.ClientError("Timeout")):
        with pytest.raises(UpdateFailed):
            await coordinator._async_update_data()


def test_sensor_properties(sensor, mock_api_data):
    """Test sensor properties."""
    sensor.coordinator.data = mock_api_data
    
    assert sensor.name == "Pont Chaban Delmas"
    assert sensor.unique_id == "chaban_bridge"
    assert sensor.state == "open"
    assert sensor.icon == "mdi:bridge"
    
    # Test closed state icon
    sensor.coordinator.data["current_state"]["is_closed"] = True
    assert sensor.icon == "mdi:bridge-off"


def test_sensor_attributes(sensor, mock_api_data):
    """Test sensor extra state attributes."""
    sensor.coordinator.data = mock_api_data
    
    attributes = sensor.extra_state_attributes
    
    assert "current_state" in attributes
    assert "is_closed" in attributes
    assert "last_update" in attributes
    assert "closures" in attributes
    assert len(attributes["closures"]) == 1


def test_sensor_device_info(sensor):
    """Test sensor device info."""
    device_info = sensor.device_info
    
    assert device_info["identifiers"] == {(DOMAIN, "chaban_bridge")}
    assert device_info["name"] == "Pont Chaban-Delmas"
    assert device_info["manufacturer"] == "Bordeaux Métropole"
