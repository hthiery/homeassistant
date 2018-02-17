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

REQUIREMENTS = ['pyfritzhome==0.3.6']

SUPPORTED_DOMAINS = ['climate', 'switch']

DOMAIN = 'fritzbox'

DEFAULT_HOST = 'fritz.box'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_DEVICES, default=[]):
            vol.All(cv.ensure_list, [dict]),
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the fritzbox component."""
    from pyfritzhome import Fritzhome, LoginError

    fritz_list = []

    if CONF_DEVICES in config[DOMAIN] and config[DOMAIN].get(CONF_DEVICES):
        configured_devices = config[DOMAIN].get(CONF_DEVICES)
        for device in configured_devices:
            try:
                host = device['host']
                username = device['username']
                password = device['password']
                fritzbox = Fritzhome(host=host, user=username, password=password)
                fritzbox.login()
                fritz_list.append(fritzbox)
                _LOGGER.info("Connected to device %s", device)
            except LoginError:
                _LOGGER.warning("Login to Fritz!Box %s as %s failed", host, username)
                continue
            except KeyError:
                _LOGGER.warning("Configuration error")
                continue

    hass.data[DOMAIN] = fritz_list

    def logout_fritzboxes(event):
        """Close all connections to the fritzboxes."""
        for fritz in fritz_list:
            fritz.logout()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, logout_fritzboxes)

    for domain in SUPPORTED_DOMAINS:
        discovery.load_platform(hass, domain, DOMAIN, {}, config)

    _LOGGER.info('Connected to fritzbox')

    return True
