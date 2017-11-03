"""
Support for AVM Fritz!Box fritzhome sensor devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/sensor.fritzhome/
"""
import logging
from datetime import timedelta

import voluptuous as vol

from custom_components.fritzhome import DATA_FRITZHOME
from homeassistant.core import callback
from homeassistant.components.sensor import ENTITY_ID_FORMAT
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    STATE_UNKNOWN, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity, generate_entity_id
from homeassistant.helpers.event import async_track_point_in_utc_time
from homeassistant.util import dt as dt_util

DEPENDENCIES = ['fritzhome']

_LOGGER = logging.getLogger(__name__)

lacrosse = None

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Fritzhome sensor component."""

    from pyfritzhome import Fritzhome

    fritz = hass.data[DATA_FRITZHOME]
    device_list = fritz.get_devices()

    sensors = []
    for device in device_list:
        if device.has_powermeter:
            sensors.append(FritzhomePowerMeter(hass, device, config))

    if not sensors:
        _LOGGER.error("No sensors added")
        return False

    add_devices(sensors)


class FritzhomePowerMeter(Entity):

    _power_in_watt = None
    _energy = None

    def __init__(self, hass, device, config):
        self.hass = hass
        self.entity_id = generate_entity_id(ENTITY_ID_FORMAT, device.id,
                                                  hass=hass)
        self._config = config
        self._value = STATE_UNKNOWN
        self._device = device

    @property
    def available(self):
        """Return if thermostat is available."""
        return self._device.present

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._device.name

    def update(self, *args):
        """Get the latest data."""
        try:
            self._power_in_watt = float(self._device.get_switch_power()/1000)
            self._energy = self._device.get_switch_energy()
        except Exception as exc:
            _LOGGER.warning("Updating the state failed: %s", exc)
        pass

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._power_in_watt

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        return attributes

    @property
    def unit_of_measurement(self):
        return 'W'

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return 'mdi:flash'
