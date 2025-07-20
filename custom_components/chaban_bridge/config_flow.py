"""Config flow for Chaban Bridge integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class ChabanBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Chaban Bridge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id("chaban_bridge")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Pont Chaban-Delmas",
                data=user_input
            )

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=DEFAULT_UPDATE_INTERVAL
                ): vol.All(int, vol.Range(min=60, max=86400)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            description_placeholders={
                "min_interval": "60",
                "max_interval": "86400",
                "default_interval": str(DEFAULT_UPDATE_INTERVAL),
            }
        )
