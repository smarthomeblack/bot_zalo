"""sendPhoto feature for Bot Zalo integration."""
import logging
from typing import Dict, Any, Optional

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class SendPhotoFeature(ZaloBotFeatureBase):
    """Feature: Send photo to chat."""

    async def execute(self, chat_id: str, photo: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """Send photo to chat."""
        _LOGGER.debug("Sending photo to chat %s: %s", chat_id, photo)
        data = {
            "chat_id": chat_id,
            "photo": photo
        }
        if caption:
            data["caption"] = caption

        return await self._make_request("sendPhoto", data)
