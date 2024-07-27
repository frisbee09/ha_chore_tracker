"""Chore Tracker - Chore Title and Description - Text"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.text import (
    TextEntity, TextEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import BINARY_SENSOR_TYPES, CONF_DATA_FEED, DEFAULT_DATA_FEED, DOMAIN
from .entity import NswFireServiceFireDangerEntity

_LOGGER = logging.getLogger(__name__)


class ChoreText(TextEntity):
    _attr_has_entity_name = True

    @property
    def translation_key(self):
        """Return the translation key to translate the entity's name and states."""
        return "common.chore.properties"

    def __init__(
            self, config_entry_id: str, chore_id: str, chore_entity_id: str,
    ):
        self.text = ""
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry_id)},
            name=f"chore_tracker_{config_entry_id}",
            entry_type=DeviceEntryType.SERVICE,
        )
        self._attr_unique_id = f"{config_entry_id}_{chore_id}_{chore_entity_id}"


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    
