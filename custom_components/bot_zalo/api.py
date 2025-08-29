"""API client for Zalo Bot integration."""
import logging
from typing import Dict, Any, Optional

from .get_me import GetMeFeature
from .set_webhook import SetWebhookFeature
from .delete_webhook import DeleteWebhookFeature
from .get_webhook_info import GetWebhookInfoFeature
from .get_updates import GetUpdatesFeature
from .send_message import SendMessageFeature
from .send_photo import SendPhotoFeature
from .send_sticker import SendStickerFeature
from .send_chat_action import SendChatActionFeature

_LOGGER = logging.getLogger(__name__)


class ZaloBotAPI:
    """Zalo Bot API client using modular features."""

    def __init__(self, bot_token: str):
        """Initialize the API client with all features."""
        self._bot_token = bot_token

        # Initialize all features
        self._get_me = GetMeFeature(bot_token)
        self._set_webhook = SetWebhookFeature(bot_token)
        self._delete_webhook = DeleteWebhookFeature(bot_token)
        self._get_webhook_info = GetWebhookInfoFeature(bot_token)
        self._get_updates = GetUpdatesFeature(bot_token)
        self._send_message = SendMessageFeature(bot_token)
        self._send_photo = SendPhotoFeature(bot_token)
        self._send_sticker = SendStickerFeature(bot_token)
        self._send_chat_action = SendChatActionFeature(bot_token)

    # Feature: getMe
    async def get_me(self) -> Dict[str, Any]:
        """Get bot information."""
        return await self._get_me.execute()

    # Feature: setWebhook
    async def set_webhook(self, webhook_url: str, secret_token: Optional[str] = None) -> Dict[str, Any]:
        """Set webhook URL."""
        return await self._set_webhook.execute(webhook_url, secret_token)

    # Feature: deleteWebhook
    async def delete_webhook(self) -> Dict[str, Any]:
        """Delete webhook."""
        return await self._delete_webhook.execute()

    # Feature: getWebhookInfo
    async def get_webhook_info(self) -> Dict[str, Any]:
        """Get webhook information."""
        return await self._get_webhook_info.execute()

    # Feature: getUpdates
    async def get_updates(self, timeout: int = 30) -> Dict[str, Any]:
        """Get updates from Zalo Bot API."""
        return await self._get_updates.execute(timeout)

    # Feature: sendMessage
    async def send_message(self, chat_id: str, text: str) -> Dict[str, Any]:
        """Send text message to chat."""
        return await self._send_message.execute(chat_id, text)

    # Feature: sendPhoto
    async def send_photo(self, chat_id: str, photo: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Send photo to chat."""
        return await self._send_photo.execute(chat_id, photo, caption)

    # Feature: sendSticker
    async def send_sticker(self, chat_id: str, sticker: str) -> Dict[str, Any]:
        """Send sticker to chat."""
        return await self._send_sticker.execute(chat_id, sticker)

    # Feature: sendChatAction
    async def send_chat_action(self, chat_id: str, action: str) -> Dict[str, Any]:
        """Send chat action to indicate bot activity."""
        return await self._send_chat_action.execute(chat_id, action)
