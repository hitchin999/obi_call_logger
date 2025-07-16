import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.event import async_track_state_change

from .const import DOMAIN, CONF_NAME, CONF_ENTITIES, CONF_ENDPOINT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    box = entry.data[CONF_NAME]
    entities = entry.data[CONF_ENTITIES]
    endpoint = entry.data[CONF_ENDPOINT]

    session = aiohttp_client.async_get_clientsession(hass)
    unsubscribers = []

    async def _on_state_change(entity_id, old, new):
        # only log when we get a WIRELESS (outgoing) call
        if new is None or not new.state.startswith("WIRELESS"):
            return

        # state: "WIRELESS CALLER 7188095414"
        number = new.state.split()[-1]
        # entity: "sensor.obihai_phone3_port_last_caller_info_3"
        port = entity_id.split(".")[1].split("_")[1]  # -> "phone3"

        payload = {"box": box, "port": port, "number": number}
        try:
            await session.post(endpoint, json=payload)
            _LOGGER.debug("Logged call %s → %s", payload, endpoint)
        except Exception as e:
            _LOGGER.error("Error logging call for %s: %s", box, e)

    # subscribe to each sensor
    for ent in entities:
        unsubscribers.append(
            async_track_state_change(hass, ent, _on_state_change)
        )

    # tidy up on unload
    entry.async_on_unload(lambda: [u() for u in unsubscribers])
    return True
