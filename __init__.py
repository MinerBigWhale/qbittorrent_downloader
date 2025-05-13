# Home Assistant qBittorrent Plugin Initialization

from homeassistant import ConfigEntries, Core, exceptions
from .const import DOMAIN, DEFAULT_CATEGORY
from .qbittorrent_api import QBittorrentAPI

async def async_setup(hass: Core, config: dict):
    """Set up the qBittorrent component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: Core, entry: ConfigEntries):
    """Set up qBittorrent from a config entry."""
    qb_api = QBittorrentAPI(entry.data['url'], entry.data['username'], entry.data['password'])
    
    if not await qb_api.test_connection():
        raise exceptions.ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = qb_api
    hass.config_entries.async_setup_platforms(entry, ["sensor", "binary_sensor"])
    
    return True

async def async_unload_entry(hass: Core, entry: ConfigEntries):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "binary_sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok