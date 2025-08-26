"""deleteWebhook feature for Bot Zalo integration."""
import logging
from typing import Dict, Any

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class DeleteWebhookFeature(ZaloBotFeatureBase):
    """Feature: Delete webhook."""

    async def execute(self) -> Dict[str, Any]:
        """Delete current webhook."""
        _LOGGER.debug("Deleting webhook")
        return await self._make_request("deleteWebhook")
