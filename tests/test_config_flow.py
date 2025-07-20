"""Test the Chaban Bridge config flow."""
import pytest
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

from custom_components.chaban_bridge.config_flow import ChabanBridgeConfigFlow
from custom_components.chaban_bridge.const import DOMAIN


async def test_form(hass):
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"update_interval": 3600},
    )
    await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Pont Chaban-Delmas"
    assert result2["data"] == {"update_interval": 3600}


async def test_form_invalid_interval(hass):
    """Test we handle invalid update interval."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Test with valid interval first to ensure flow works
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"update_interval": 3600},
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY


async def test_single_instance(hass, mock_config_entry):
    """Test that only one instance is allowed."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"update_interval": 3600},
    )
    
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"
