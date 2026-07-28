"""Charge station sensor implementation."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import EnbwConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: EnbwConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:  # pylint disable=unused-argument
    """Set up EnBw Charge station via config entry."""
    station = config_entry.runtime_data
    async_add_entities(station.binary_sensors)
