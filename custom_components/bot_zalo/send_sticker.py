"""sendSticker feature for Bot Zalo integration."""
import logging
from typing import Dict, Any

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class SendStickerFeature(ZaloBotFeatureBase):
    """Feature: Send sticker to chat."""

    async def execute(self, chat_id: str, sticker: str) -> Dict[str, Any]:
        """Send sticker to chat."""
        _LOGGER.debug("Sending sticker to chat %s: %s", chat_id, sticker)
        data = {
            "chat_id": chat_id,
            "sticker": sticker
        }
        return await self._make_request("sendSticker", data)
