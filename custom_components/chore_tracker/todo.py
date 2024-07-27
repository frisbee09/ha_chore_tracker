"""Chore Tracker implementing a ToDo entity."""

import datetime
from functools import cached_property
import logging

from homeassistant.components.todo import TodoItem, TodoListEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)


class ChoreTrackerToDo(TodoItem):
    """Representation of a Chore Tracker ToDo entity."""

    effort_weight: int | None = None
    """The relative effort of the chore to complete."""

    last_completed_by: str | None = None
    """The name of the person who completed the chore last."""

    last_completed_date: datetime.date | datetime.datetime | None = None
    """When the chore was last completed."""

    cadence: int | None = None
    """The number of days between the chore being completed and the completion
    state decaying."""

    order: int | None = None


class ChoreTrackerToDoList(TodoListEntity):
    """Representation of a Chore Tracker ToDo entity."""

    _attr_todo_items: dict[str, ChoreTrackerToDo] = {}

    def __init__(
        self,
        chore_group_name: str,
        todos: list[ChoreTrackerToDo] | None = None,
        config_entry_unique_id: str | None = None,
    ) -> None:
        """Initialize the Chore Tracker ToDo entity."""
        self.name = chore_group_name
        self._attr_unique_id = config_entry_unique_id

        if todos is not None:
            self._attr_todo_items = {todo.uid: todo for todo in todos}

    # pylint: disable=hass-return-type
    @cached_property
    def todo_items(self) -> list[ChoreTrackerToDo] | None:
        """Return the list of Chore Tracker ToDo items."""
        list_of_todos = list(self._attr_todo_items.values())
        list_of_todos.sort(key=lambda x: (x.order, x.summary))
        return list_of_todos

    async def async_create_todo_item(self, item: TodoItem) -> None:
        """Create a new Chore Tracker ToDo item."""
        self._attr_todo_items[item.uid] = item

    async def async_update_todo_item(self, item: TodoItem) -> None:
        """Update an existing Chore Tracker ToDo item."""
        self._attr_todo_items[item.uid] = item

    async def async_delete_todo_items(self, uids: list[str]) -> None:
        """Delete Chore Tracker ToDo items."""
        self._attr_todo_items = {
            uid: item for uid, item in self._attr_todo_items.items() if uid not in uids
        }

    async def async_move_todo_item(
        self, uid: str, previous_uid: str | None = None
    ) -> None:
        """Move a Chore Tracker ToDo item."""
        self._attr_todo_items[uid].order, self._attr_todo_items[previous_uid].order = (
            self._attr_todo_items[previous_uid].order,
            self._attr_todo_items[uid].order,
        )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Chore Tracker ToDo list."""
    chore_group_name = config_entry.data["chore_group_name"]
    config_entry_unique_id = config_entry.unique_id
    todos = config_entry.data.get("todos", [])

    async_add_entities(
        [
            ChoreTrackerToDoList(
                chore_group_name,
                [ChoreTrackerToDo(**todo) for todo in todos],
                config_entry_unique_id,
            )
        ]
    )
