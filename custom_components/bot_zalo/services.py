"""Services for Bot Zalo integration."""
import voluptuous as vol
import logging
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
import homeassistant.helpers.config_validation as cv
from .const import (
    DOMAIN,
    SERVICE_SEND_MESSAGE,
    SERVICE_SEND_PHOTO,
    SERVICE_SEND_STICKER,
    SERVICE_SET_WEBHOOK,
    SERVICE_DELETE_WEBHOOK,
    SERVICE_GET_ME,
    SERVICE_GET_WEBHOOK_INFO,
    ATTR_CHAT_ID,
    ATTR_TEXT,
    ATTR_PHOTO,
    ATTR_CAPTION,
    ATTR_STICKER,
    ATTR_WEBHOOK_URL,
    ATTR_SECRET_TOKEN
)
from .api import ZaloBotAPI

_LOGGER = logging.getLogger(__name__)

# Service schemas
SEND_MESSAGE_SCHEMA = vol.Schema({
    vol.Required(ATTR_CHAT_ID): cv.string,
    vol.Required(ATTR_TEXT): cv.string,
})

SEND_PHOTO_SCHEMA = vol.Schema({
    vol.Required(ATTR_CHAT_ID): cv.string,
    vol.Required(ATTR_PHOTO): cv.string,
    vol.Optional(ATTR_CAPTION): cv.string,
})

SEND_STICKER_SCHEMA = vol.Schema({
    vol.Required(ATTR_CHAT_ID): cv.string,
    vol.Required(ATTR_STICKER): cv.string,
})

SET_WEBHOOK_SCHEMA = vol.Schema({
    vol.Required(ATTR_WEBHOOK_URL): cv.url,
    vol.Optional(ATTR_SECRET_TOKEN): cv.string,
})


async def async_setup_services(hass: HomeAssistant, api: ZaloBotAPI) -> None:
    """Set up services for Bot Zalo."""

    async def send_message_service(call: ServiceCall) -> ServiceResponse:
        """Handle send_message service call."""
        chat_id = call.data[ATTR_CHAT_ID]
        text = call.data[ATTR_TEXT]

        try:
            result = await api.send_message(chat_id, text)
            _LOGGER.info("Message sent successfully: %s", result)
            return {
                "success": result.get("ok", False),
                "chat_id": chat_id,
                "text": text,
                "message_id": result.get("result", {}).get("message_id"),
                "date": result.get("result", {}).get("date"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to send message: %s", err)
            return {
                "success": False,
                "chat_id": chat_id,
                "text": text,
                "error": str(err)
            }

    async def send_photo_service(call: ServiceCall) -> ServiceResponse:
        """Handle send_photo service call."""
        chat_id = call.data[ATTR_CHAT_ID]
        photo = call.data[ATTR_PHOTO]
        caption = call.data.get(ATTR_CAPTION)

        try:
            result = await api.send_photo(chat_id, photo, caption)
            _LOGGER.info("Photo sent successfully: %s", result)
            return {
                "success": result.get("ok", False),
                "chat_id": chat_id,
                "photo": photo,
                "caption": caption,
                "message_id": result.get("result", {}).get("message_id"),
                "date": result.get("result", {}).get("date"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to send photo: %s", err)
            return {
                "success": False,
                "chat_id": chat_id,
                "photo": photo,
                "caption": caption,
                "error": str(err)
            }

    async def send_sticker_service(call: ServiceCall) -> ServiceResponse:
        """Handle send_sticker service call."""
        chat_id = call.data[ATTR_CHAT_ID]
        sticker = call.data[ATTR_STICKER]

        try:
            result = await api.send_sticker(chat_id, sticker)
            _LOGGER.info("Sticker sent successfully: %s", result)
            return {
                "success": result.get("ok", False),
                "chat_id": chat_id,
                "sticker": sticker,
                "message_id": result.get("result", {}).get("message_id"),
                "date": result.get("result", {}).get("date"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to send sticker: %s", err)
            return {
                "success": False,
                "chat_id": chat_id,
                "sticker": sticker,
                "error": str(err)
            }

    async def set_webhook_service(call: ServiceCall) -> ServiceResponse:
        """Handle set_webhook service call."""
        webhook_url = call.data[ATTR_WEBHOOK_URL]
        secret_token = call.data.get(ATTR_SECRET_TOKEN)

        try:
            result = await api.set_webhook(webhook_url, secret_token)
            _LOGGER.info("Webhook set successfully: %s", result)
            return {
                "success": result.get("ok", False),
                "webhook_url": webhook_url,
                "secret_token": secret_token,
                "updated_at": result.get("result", {}).get("updated_at"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to set webhook: %s", err)
            return {
                "success": False,
                "webhook_url": webhook_url,
                "secret_token": secret_token,
                "error": str(err)
            }

    async def delete_webhook_service(call: ServiceCall) -> ServiceResponse:
        """Handle delete_webhook service call."""
        try:
            result = await api.delete_webhook()
            _LOGGER.info("Webhook deleted successfully: %s", result)
            return {
                "success": result.get("ok", False),
                "updated_at": result.get("result", {}).get("updated_at"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to delete webhook: %s", err)
            return {
                "success": False,
                "error": str(err)
            }

    async def get_me_service(call: ServiceCall) -> ServiceResponse:
        """Handle get_me service call."""
        try:
            result = await api.get_me()
            _LOGGER.info("Bot info retrieved: %s", result)
            bot_info = result.get("result", {})
            return {
                "success": result.get("ok", False),
                "id": bot_info.get("id"),
                "account_name": bot_info.get("account_name"),
                "account_type": bot_info.get("account_type"),
                "can_join_groups": bot_info.get("can_join_groups"),
                "display_name": bot_info.get("display_name"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to get bot info: %s", err)
            return {
                "success": False,
                "error": str(err)
            }

    async def get_webhook_info_service(call: ServiceCall) -> ServiceResponse:
        """Handle get_webhook_info service call."""
        try:
            result = await api.get_webhook_info()
            _LOGGER.info("Webhook info retrieved: %s", result)
            webhook_info = result.get("result", {})
            return {
                "success": result.get("ok", False),
                "url": webhook_info.get("url"),
                "updated_at": webhook_info.get("updated_at"),
                "full_response": result
            }
        except Exception as err:
            _LOGGER.error("Failed to get webhook info: %s", err)
            return {
                "success": False,
                "error": str(err)
            }

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_MESSAGE,
        send_message_service,
        schema=SEND_MESSAGE_SCHEMA,
        supports_response=SupportsResponse.ONLY
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_PHOTO,
        send_photo_service,
        schema=SEND_PHOTO_SCHEMA,
        supports_response=SupportsResponse.ONLY
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_STICKER,
        send_sticker_service,
        schema=SEND_STICKER_SCHEMA,
        supports_response=SupportsResponse.ONLY
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_WEBHOOK,
        set_webhook_service,
        schema=SET_WEBHOOK_SCHEMA,
        supports_response=SupportsResponse.ONLY
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_WEBHOOK,
        delete_webhook_service,
        supports_response=SupportsResponse.ONLY
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_ME,
        get_me_service,
        supports_response=SupportsResponse.ONLY
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_WEBHOOK_INFO,
        get_webhook_info_service,
        supports_response=SupportsResponse.ONLY
    )

    _LOGGER.info("Bot Zalo services registered successfully")
