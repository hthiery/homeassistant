"""
Support for AVM Fritz!Box smarthome devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/fritzbox/
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_DEVICES, CONF_HOST, CONF_PASSWORD, CONF_USERNAME,
    EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyfritzhome==0.3.7']

SUPPORTED_DOMAINS = ['climate', 'switch']

DOMAIN = 'fritzbox'

ATTR_STATE_DEVICE_LOCKED = 'device_locked'
ATTR_STATE_LOCKED = 'locked'
ATTR_STATE_BATTERY_LOW = 'battery_low'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICES, default=[]):
            vol.All(cv.ensure_list, [
                vol.Schema({
                    vol.Required(CONF_HOST): cv.string,
                    vol.Required(CONF_PASSWORD): cv.string,
                    vol.Required(CONF_USERNAME): cv.string,
                }),
            ]),
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the fritzbox component."""
    from pyfritzhome import Fritzhome, LoginError

    fritz_list = []

    configured_devices = config[DOMAIN].get(CONF_DEVICES)
    for device in configured_devices:
        try:
            host = device.get(CONF_HOST)
            username = device.get(CONF_USERNAME)
            password = device.get(CONF_PASSWORD)
            fritzbox = Fritzhome(host=host, user=username,
                                 password=password)
            fritzbox.login()
            fritz_list.append(fritzbox)
            _LOGGER.info("Connected to device %s", device)
        except LoginError:
            _LOGGER.warning("Login to Fritz!Box %s as %s failed",
                            host, username)
            continue

    if not fritz_list:
        return False

    hass.data[DOMAIN] = fritz_list

    def logout_fritzboxes(event):
        """Close all connections to the fritzboxes."""
        for fritz in fritz_list:
            fritz.logout()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, logout_fritzboxes)

    for domain in SUPPORTED_DOMAINS:
        discovery.load_platform(hass, domain, DOMAIN, {}, config)

    return True
