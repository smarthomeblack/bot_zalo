"""Config flow for Bot Zalo integration."""
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from .const import (
    DOMAIN,
    CONF_BOT_TOKEN,
)
from .api import ZaloBotAPI

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_BOT_TOKEN): cv.string,
})


class BotZaloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bot Zalo."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate credentials by calling getMe API
            try:
                await self._test_credentials(
                    user_input[CONF_BOT_TOKEN]
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "unknown"
            else:
                # Create unique ID based on bot_token hash
                import hashlib
                token_hash = hashlib.md5(user_input[CONF_BOT_TOKEN].encode()).hexdigest()[:8]
                await self.async_set_unique_id(token_hash)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Bot Zalo ({token_hash})",
                    data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors
        )

    async def _test_credentials(self, bot_token: str):
        """Test if we can authenticate with the Zalo API."""
        try:
            api = ZaloBotAPI(bot_token=bot_token)

            # Test getMe endpoint
            result = await api.get_me()

            # Check if response is valid according to Zalo Bot API format
            if not result:
                raise InvalidAuth("No response from Zalo API")

            if not result.get("ok"):
                # API returned error
                error_msg = result.get("description", "Invalid bot token")
                raise InvalidAuth(f"Zalo API error: {error_msg}")

            if not result.get("result"):
                raise InvalidAuth("Invalid response format from Zalo API")

            # Validate that we got bot info
            bot_info = result["result"]
            if not bot_info.get("id") or not bot_info.get("account_name"):
                raise InvalidAuth("Invalid bot information received")

            return True

        except InvalidAuth:
            # Re-raise authentication errors
            raise
        except Exception as err:
            # Convert other errors to connection errors
            raise CannotConnect(f"Failed to connect to Zalo API: {err}")


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
