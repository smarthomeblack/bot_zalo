"""getWebhookInfo feature for Bot Zalo integration."""
import logging
from typing import Dict, Any

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class GetWebhookInfoFeature(ZaloBotFeatureBase):
    """Feature: Get webhook information."""

    async def execute(self) -> Dict[str, Any]:
        """Get webhook information from Zalo Bot API."""
        _LOGGER.debug("Getting webhook information")
        return await self._make_request("getWebhookInfo")
