import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_NAME, CONF_ENTITIES, CONF_ENDPOINT

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): str,
    vol.Required(CONF_ENTITIES): cv.entity_ids,
    vol.Required(CONF_ENDPOINT): str,
})

class ObiCallLoggerFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=DATA_SCHEMA
            )

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data=user_input
        )
