"""sendMessage feature for Bot Zalo integration."""
import logging
from typing import Dict, Any

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class SendMessageFeature(ZaloBotFeatureBase):
    """Feature: Send text message."""

    async def execute(self, chat_id: str, text: str) -> Dict[str, Any]:
        """Send text message to chat."""
        _LOGGER.debug("Sending message to chat %s: %s", chat_id, text)
        data = {
            "chat_id": chat_id,
            "text": text
        }
        return await self._make_request("sendMessage", data)
