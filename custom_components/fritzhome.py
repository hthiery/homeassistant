"""
Support for AVM Fritz!Box fritzhome devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/fritzhome/
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST, CONF_PASSWORD, CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyfritzhome==0.3.4']

DOMAIN = 'fritzhome'

DEFAULT_HOST = 'fritz.box'

ATTR_DISCOVERY_SENSORS = 'sensors'
ATTR_DISCOVERY_SWITCHES = 'switches'
ATTR_DISCOVERY_THERMOSTATES = 'thermostates'

ATTR_AIN = 'ain'
ATTR_ID = 'id'
ATTR_FW_VERSION = 'firmware_version'
ATTR_MANUFACTURER = 'manufacturer'
ATTR_PRODUCTNAME = 'product_name'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the fritzhome component."""
    from pyfritzhome import Fritzhome, LoginError

    conf = config[DOMAIN]
    host = conf.get(CONF_HOST)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)

    devices = None
    try:
        fritz = Fritzhome(host=host, user=username, password=password)
        fritz.login()
        devices = fritz.get_devices()
    except LoginError:
        _LOGGER.warning("Login to Fritz!Box failed")
        return False

    _LOGGER.info('Connected to Fritz!Box')

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, fritz.logout)

    discovery.load_platform(hass, 'climate', DOMAIN, 
        {ATTR_DISCOVERY_THERMOSTATES: [d for d in devices if d.has_thermostat]}, config)

    discovery.load_platform(hass, 'sensor', DOMAIN,
        {ATTR_DISCOVERY_SENSORS: devices}, config)

    discovery.load_platform(hass, 'switch', DOMAIN,
        {ATTR_DISCOVERY_SWITCHES: [d for d in devices if d.has_switch]}, config)


    return True
