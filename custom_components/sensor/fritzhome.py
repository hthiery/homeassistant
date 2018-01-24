"""
Support for AVM Fritz!Box fritzhome sensor devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/sensor.fritzhome/
"""
import logging

import requests

from custom_components.fritzhome import DOMAIN as FRITZHOME_DOMAIN
from homeassistant.helpers.entity import Entity

DEPENDENCIES = ['fritzhome']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Fritzhome sensor component."""
    fritz = hass.data[FRITZHOME_DOMAIN]
    device_list = fritz.get_devices()

    sensors = []
    for device in device_list:
        if device.has_powermeter:
            sensors.append(FritzhomePowerMeter(device, config))

    if not sensors:
        _LOGGER.error("No sensors added")
        return False

    add_devices(sensors)


class FritzhomePowerMeter(Entity):
    """Implementation of a Fritzhome power meter sensor."""
    _power_in_watt = None
    _energy = None

    def __init__(self, device, fritz):
        self._device = device
        self._fritz = fritz
        self._power = None

    @property
    def available(self):
        """Return if thermostat is available."""
        return self._device.present

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._device.name

    def update(self):
        """Get the latest data."""
        try:
            self._device.update()
            self._power = self._device.power
        except requests.exceptions.HTTPError as ex:
            _LOGGER.warning("Fritzhome connection error: %s", ex)
            self._fritz.login()
            self._power = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._power

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'W'

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return 'mdi:flash'
