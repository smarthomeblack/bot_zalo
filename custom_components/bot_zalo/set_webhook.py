"""setWebhook feature for Bot Zalo integration."""
import logging
from typing import Dict, Any, Optional

from .base import ZaloBotFeatureBase

_LOGGER = logging.getLogger(__name__)


class SetWebhookFeature(ZaloBotFeatureBase):
    """Feature: Set webhook URL."""

    async def execute(self, webhook_url: str, secret_token: Optional[str] = None) -> Dict[str, Any]:
        """Set webhook URL for receiving messages."""
        _LOGGER.debug("Setting webhook URL: %s", webhook_url)
        data = {
            "url": webhook_url
        }
        if secret_token:
            data["secret_token"] = secret_token

        return await self._make_request("setWebhook", data)
