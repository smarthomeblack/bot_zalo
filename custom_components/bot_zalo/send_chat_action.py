"""sendChatAction feature for Bot Zalo integration."""
import logging
from typing import Dict, Any

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class SendChatActionFeature(ZaloBotFeatureBase):
    """Feature: Send chat action (typing indicator)."""

    async def execute(self, chat_id: str, action: str) -> Dict[str, Any]:
        """Send chat action to indicate bot activity."""
        _LOGGER.debug("Sending chat action '%s' to chat %s", action, chat_id)
        data = {
            "chat_id": chat_id,
            "action": action
        }
        return await self._make_request("sendChatAction", data)
