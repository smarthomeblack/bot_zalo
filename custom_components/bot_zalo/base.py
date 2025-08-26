"""Base class for Bot Zalo features."""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import aiohttp

_LOGGER = logging.getLogger(__name__)


class ZaloBotFeatureBase(ABC):
    """Base class for all Zalo Bot features."""

    def __init__(self, bot_token: str):
        """Initialize the feature."""
        self._bot_token = bot_token
        self._base_url = f"https://bot-api.zapps.me/bot{bot_token}"
        self._headers = {
            "Content-Type": "application/json"
        }

    async def _make_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an API request."""
        url = f"{self._base_url}/{endpoint}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url,
                    headers=self._headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    _LOGGER.debug("Response status: %s", response.status)
                    _LOGGER.debug("Response headers: %s", dict(response.headers))

                    # Get response text first since Zalo API may not set Content-Type
                    response_text = await response.text()
                    _LOGGER.debug("Response text: %s", response_text)

                    # Parse JSON manually since aiohttp.json() fails without Content-Type
                    try:
                        import json
                        response_data = json.loads(response_text)
                    except json.JSONDecodeError as json_err:
                        _LOGGER.error("Failed to parse JSON. Response: %s", response_text)
                        return {"ok": False, "error": f"JSON parse error: {json_err}"}

                    if response.status != 200:
                        _LOGGER.error(
                            "API request failed: %s - Status: %s, Response: %s",
                            url, response.status, response_data
                        )

                    return response_data

            except aiohttp.ClientError as err:
                _LOGGER.error("API request error: %s", err)
                raise
            except Exception as err:
                _LOGGER.error("Unexpected error: %s", err)
                raise

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the feature functionality."""
        pass
