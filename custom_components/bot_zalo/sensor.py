"""Sensor platform for Bot Zalo integration."""
from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN
from .api import ZaloBotAPI

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    api = data["api"]
    coordinator = BotZaloDataUpdateCoordinator(hass, api, config_entry)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Add entities
    async_add_entities([
        BotZaloInfoSensor(coordinator, config_entry),
        BotZaloWebhookSensor(coordinator, config_entry)
    ])


class BotZaloDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Zalo API."""

    def __init__(self, hass: HomeAssistant, api: ZaloBotAPI, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self.api = api
        self.config_entry = config_entry
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Update data via Zalo API."""
        try:
            # Get bot info
            bot_info = await self.api.get_me()

            # Get webhook info
            webhook_info = await self.api.get_webhook_info()

            return {
                "bot_info": bot_info,
                "webhook_info": webhook_info,
                "last_update": self.hass.loop.time()
            }
        except Exception as exception:
            _LOGGER.error("Error fetching data from Zalo API: %s", exception)
            raise


class BotZaloInfoSensor(CoordinatorEntity, SensorEntity):
    """Representation of Bot Zalo info sensor."""

    def __init__(self, coordinator: BotZaloDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Bot Zalo Info"
        self._attr_unique_id = f"{config_entry.entry_id}_bot_info"
        self._attr_icon = "mdi:robot"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        bot_info = self.coordinator.data.get("bot_info", {})
        if bot_info and bot_info.get("ok") and "result" in bot_info:
            return bot_info["result"].get("display_name", "Unknown")
        return "Unavailable"

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        bot_info = self.coordinator.data.get("bot_info", {})
        if bot_info and bot_info.get("ok") and "result" in bot_info:
            result = bot_info["result"]
            return {
                "id": result.get("id"),
                "account_name": result.get("account_name"),
                "display_name": result.get("display_name"),
                "account_type": result.get("account_type"),
                "can_join_groups": result.get("can_join_groups"),
                "status": "Active"
            }
        return {"status": "Unavailable"}

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": "Bot Zalo",
            "manufacturer": "smarthomeblack",
            "model": "Official Bot Zalo",
            "sw_version": "2025.8.26",
        }


class BotZaloWebhookSensor(CoordinatorEntity, SensorEntity):
    """Representation of Bot Zalo webhook sensor."""

    def __init__(self, coordinator: BotZaloDataUpdateCoordinator, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Bot Zalo Webhook"
        self._attr_unique_id = f"{config_entry.entry_id}_webhook"
        self._attr_icon = "mdi:webhook"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        webhook_info = self.coordinator.data.get("webhook_info", {})
        if webhook_info and webhook_info.get("ok") and "result" in webhook_info:
            webhook_url = webhook_info["result"].get("url")
            return "Active" if webhook_url else "Inactive"
        return "Unknown"

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        webhook_info = self.coordinator.data.get("webhook_info", {})
        if webhook_info and webhook_info.get("ok") and "result" in webhook_info:
            result = webhook_info["result"]
            return {
                "url": result.get("url"),
                "updated_at": result.get("updated_at"),
                "status": "Active" if result.get("url") else "Inactive",
                "last_update": self.coordinator.data.get("last_update")
            }
        return {"status": "Unknown"}

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "name": "Bot Zalo",
            "manufacturer": "Zalo",
            "model": "Official Account Bot",
            "sw_version": "1.0.0",
        }
