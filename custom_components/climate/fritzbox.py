"""
Support for AVM Fritz!Box smarthome thermostate devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/climate.fritzbox/
"""
import logging

import requests

from custom_components.fritzbox import DOMAIN as FRITZBOX_DOMAIN
from custom_components.fritzbox import (
    ATTR_STATE_DEVICE_LOCKED, ATTR_STATE_BATTERY_LOW, ATTR_STATE_LOCKED)
from homeassistant.components.climate import (
    ATTR_OPERATION_MODE, ClimateDevice, STATE_ECO, STATE_HEAT,
    SUPPORT_OPERATION_MODE, SUPPORT_TARGET_TEMPERATURE)
from homeassistant.const import (
    ATTR_TEMPERATURE, PRECISION_HALVES, TEMP_CELSIUS)

DEPENDENCIES = ['fritzbox']

_LOGGER = logging.getLogger(__name__)

STATE_MANUAL = 'manual'

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE)

OPERATION_LIST = [STATE_HEAT, STATE_ECO]

MIN_TEMPERATURE = 8
MAX_TEMPERATURE = 28


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Fritzbox smarthome thermostat platform."""
    devices = []
    fritz_list = hass.data[FRITZBOX_DOMAIN]

    for fritz in fritz_list:
        device_list = fritz.get_devices()
        for device in device_list:
            if device.has_thermostat:
                devices.append(FritzboxThermostat(device, fritz))

    add_devices(devices)


class FritzboxThermostat(ClimateDevice):
    """The thermostat class for Fritzbox smarthome thermostates."""

    def __init__(self, device, fritz):
        """Initialize the thermostat."""
        self._device = device
        self._fritz = fritz
        self._current_temperature = self._device.actual_temperature
        self._target_temperature = self._device.target_temperature
        self._comfort_temperature = self._device.comfort_temperature
        self._eco_temperature = self._device.eco_temperature

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def available(self):
        """Return if thermostat is available."""
        return self._device.present

    @property
    def name(self):
        """Return the name of the device."""
        return self._device.name

    @property
    def temperature_unit(self):
        """Return the unit of measurement that is used."""
        return TEMP_CELSIUS

    @property
    def precision(self):
        """Return precision 0.5."""
        return PRECISION_HALVES

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        if ATTR_OPERATION_MODE in kwargs:
            operation_mode = kwargs.get(ATTR_OPERATION_MODE)
            self.set_operation_mode(operation_mode)
        elif ATTR_TEMPERATURE in kwargs:
            temperature = kwargs.get(ATTR_TEMPERATURE)
            self._device.set_target_temperature(temperature)

    @property
    def current_operation(self):
        """Return the current operation mode."""
        if self._target_temperature == self._comfort_temperature:
            return STATE_HEAT
        elif self._target_temperature == self._eco_temperature:
            return STATE_ECO
        return STATE_MANUAL

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return OPERATION_LIST

    def set_operation_mode(self, operation_mode):
        """Set new operation mode."""
        if operation_mode == STATE_HEAT:
            self.set_temperature(temperature=self._comfort_temperature)
        elif operation_mode == STATE_ECO:
            self.set_temperature(temperature=self._eco_temperature)

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return MIN_TEMPERATURE

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return MAX_TEMPERATURE

    @property
    def device_state_attributes(self):
        """Return the device specific state attributes."""
        attrs = {
            ATTR_STATE_DEVICE_LOCKED: self._device.device_lock,
            ATTR_STATE_LOCKED: self._device.lock,
            ATTR_STATE_BATTERY_LOW: self._device.battery_low,
        }
        return attrs

    def update(self):
        """Update the data from the thermostat."""
        try:
            self._device.update()
            self._current_temperature = self._device.actual_temperature
            self._target_temperature = self._device.target_temperature
            self._comfort_temperature = self._device.comfort_temperature
            self._eco_temperature = self._device.eco_temperature
        except requests.exceptions.HTTPError as ex:
            _LOGGER.warning("Fritzbox connection error: %s", ex)
            self._fritz.login()
