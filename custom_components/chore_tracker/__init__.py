"""The Chore Tracker integration."""

from __future__ import annotations

from datetime import datetime
import logging
from typing import TypedDict

from homeassistant.components.chore_tracker.todo import ChoreTrackerToDoList
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[Platform] = [
    Platform.TODO,
]


class ChoreListConfigData(TypedDict):
    """TypedDict for Chore Tracker Coordinator Data."""

    chore_group_name: str


type ChoreListConfigEntry = ConfigEntry[ChoreListConfigData]  # noqa: F821


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Chore Tracker component."""
    component = hass.data[DOMAIN] = EntityComponent[ChoreTrackerToDoList](
        _LOGGER, DOMAIN, hass, datetime.timedelta(seconds=60)
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ChoreListConfigEntry) -> bool:
    """Set up Chore Tracker from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ChoreListConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
