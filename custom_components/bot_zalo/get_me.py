"""getMe feature for Bot Zalo integration."""
import logging
from typing import Dict, Any

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class GetMeFeature(ZaloBotFeatureBase):
    """Feature: Get bot information."""

    async def execute(self) -> Dict[str, Any]:
        """Get bot information from Zalo Bot API."""
        _LOGGER.debug("Getting bot information")
        return await self._make_request("getMe")
