"""Config flow for Chore Tracker integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required("chore_group_name"): str})


class ChoreTrackerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Chore Tracker."""

    VERSION = 1

    async def _show_group_selection_form(self):
        data_schema = vol.Schema(
            {
                vol.Required("chore_group_name"): str,
            }
        )

    async def _show_reconfiguration_menu(self):
        return self.async_show_menu(
            step_id="reconfigure",
            menu_options={"edit_existing_cg": "edit_existing_cg", "new_cg": "new_cg"},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        await self.async_set_unique_id(user_input["chore_group_name"])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=user_input["chore_group_name"], data=user_input
        )

    async_step_new_cg = async_step_user

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration of the integration."""
        if user_input is None:
            return self._show_reconfiguration_menu()

        return await self.async_step_user(user_input)
