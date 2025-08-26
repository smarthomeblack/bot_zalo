"""getUpdates feature for Bot Zalo integration."""
import logging
from typing import Dict, Any, Optional

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class GetUpdatesFeature(ZaloBotFeatureBase):
    """Feature: Get updates from Zalo Bot API."""

    async def execute(self, timeout: Optional[int] = 30) -> Dict[str, Any]:
        """Get updates from Zalo Bot API."""
        _LOGGER.debug("Getting updates with timeout %s", timeout)
        data = {}
        if timeout is not None:
            data["timeout"] = timeout

        return await self._make_request("getUpdates", data)
