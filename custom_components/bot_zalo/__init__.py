"""
Bot Zalo integration for Home Assistant.

This integration provides Zalo Bot functionality.
"""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_BOT_TOKEN
from .api import ZaloBotAPI
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bot Zalo from a config entry."""
    _LOGGER.info("Setting up Bot Zalo integration")

    # Get configuration
    bot_token = entry.data[CONF_BOT_TOKEN]

    # Create API instance
    api = ZaloBotAPI(bot_token=bot_token)

    # Store API instance
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "config": entry.data
    }

    # Setup services
    await async_setup_services(hass, api)

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Bot Zalo integration")

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Remove stored data
        hass.data[DOMAIN].pop(entry.entry_id)

        # Remove services if this is the last entry
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, "send_message")
            hass.services.async_remove(DOMAIN, "send_photo")
            hass.services.async_remove(DOMAIN, "send_sticker")
            hass.services.async_remove(DOMAIN, "set_webhook")
            hass.services.async_remove(DOMAIN, "delete_webhook")
            hass.services.async_remove(DOMAIN, "get_me")
            hass.services.async_remove(DOMAIN, "get_webhook_info")

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
