"""Custom integration for EnBW Charge Stations."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.device_registry import DeviceEntry

from .charge_station import ChargeStation
from .const import API_KEY, NAME, STATION_NUMBER

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

type EnbwConfigEntry = ConfigEntry[ChargeStation]


async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: EnbwConfigEntry,
    device_entry: DeviceEntry,
) -> bool:  # pylint: disable=unused-argument
    """Remove a config entry from a device."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: EnbwConfigEntry) -> bool:
    """Set up EnBW Charge Station from a config entry."""
    station = ChargeStation(
        hass,
        entry.data.get(NAME),
        entry.data.get(STATION_NUMBER),
        entry.data.get(API_KEY),
    )
    if not await hass.async_add_executor_job(station.update):
        raise ConfigEntryNotReady(
            f"Unable to fetch data for charge station {entry.data.get(STATION_NUMBER)}"
        )
    entry.runtime_data = station

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EnbwConfigEntry) -> bool:
    """Unload a config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
