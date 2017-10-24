import asyncio
import logging
import voluptuous as vol
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST, CONF_PASSWORD, CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyfritzhome']

DATA_FRITZHOME = 'fritzhome_api'
SUPPORTED_DOMAINS = ['climate', 'switch']

DOMAIN = 'fritzhome'

DEFAULT_HOST = 'fritz.box'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Setup the fritzhome component."""

    from pyfritzhome import Fritzhome, LoginError
    conf = config[DOMAIN]
    host = conf.get(CONF_HOST, DEFAULT_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    try:
        fritz = Fritzhome(host=host, user=username, password=password)
        fritz.login()
        hass.data[DATA_FRITZHOME] = fritz
    except LoginError:
        _LOGGER.error("Login to Fritz!Box failed")
        return False

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP,
                         logout)

    devices = fritz.get_devices()
    for device in devices:
        _LOGGER.warning(device.name)

    _LOGGER.warning('connected to fritzbox')

    return True

def logout():
    """Close the session to the fritzbox."""
    pass
