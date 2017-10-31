"""
Support for AVM Fritz!Box fritzhome devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/fritzhome/
"""
import logging

import voluptuous as vol

from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST, CONF_PASSWORD, CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyfritzhome==0.2.4']

DATA_FRITZHOME = 'fritzhome_api'
SUPPORTED_DOMAINS = ['climate', 'switch']

DOMAIN = 'fritzhome'

DEFAULT_HOST = 'fritz.box'

ATTR_FW_VERSION = 'firmware_verson'
ATTR_MANUFACTURER = 'manufacturer'
ATTR_PRODUCTNAME = 'product_name'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the fritzhome component."""
    from pyfritzhome import Fritzhome, LoginError

    conf = config[DOMAIN]
    host = conf.get(CONF_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    try:
        fritz = Fritzhome(host=host, user=username, password=password)
        fritz.login()
        hass.data[DATA_FRITZHOME] = fritz
    except LoginError:
        _LOGGER.warning("Login to Fritz!Box failed")
        return False

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, fritz.logout)

    _LOGGER.info('Connected to fritzbox')

    return True
