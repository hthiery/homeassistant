import logging

from custom_components.fritzhome import DATA_FRITZHOME
from homeassistant.components.climate import (
    ClimateDevice, PRECISION_HALVES, STATE_ECO,
)
from homeassistant.const import (TEMP_CELSIUS,)

DEPENDENCIES = ['fritzhome']

_LOGGER = logging.getLogger(__name__)

STATE_COMFORT = 'comfort'

OPERATION_LIST = [STATE_ECO, STATE_COMFORT]


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set the Fritzhome thermostat platform."""

    if DATA_FRITZHOME not in hass.data:
        return False

    _LOGGER.warning("setup_platform climate")

    fritz = hass.data[DATA_FRITZHOME]
    device_list = fritz.get_devices()

    devices = []
    for device in device_list:
        _LOGGER.warning(device.name)
        if device.has_thermostat:
            devices.append(FritzhomeThermostat(device))

    add_devices(devices)


class FritzhomeThermostat(ClimateDevice):
    """The thermostat class for Fritzhome."""

    def __init__(self, device):
        self._device = device
        self._temperature = None
        self._target_temperature = None
        self._eco_temperature = None
        self._comfort_temperature = None

    @property
    def available(self):
        """Return if thermostat is available."""
        return self._device.get_present()

#    @property
#    def should_poll(self):
#        return True

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
        """Can not report temperature, so return target_temperature."""
        return self._temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

#    def set_temperature(self, **kwargs):
#        """Set new target temperature."""
#        temperature = kwargs.get(ATTR_TEMPERATURE)
#        if temperature is None:
#            return
#        self._thermostat.target_temperature = temperature

    @property
    def current_operation(self):
        """Return the current operation mode."""
        if not self.available:
            return None
        if self._target_temperature == self._comfort_temperature:
            return STATE_COMFORT
        elif self._target_temperature == self._eco_temperature:
            return STATE_ECO
        return 'unknown'

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return OPERATION_LIST

#    def set_operation_mode(self, operation_mode):
#        """Set operation mode."""
#        self._thermostat.mode = self.reverse_modes[operation_mode]

#    def turn_away_mode_off(self):
#        """Away mode off turns to AUTO mode."""
#        self.set_operation_mode(STATE_AUTO)

#    def turn_away_mode_on(self):
#        """Set away mode on."""
#        self.set_operation_mode(STATE_AWAY)

#    @property
#    def is_away_mode_on(self):
#        """Return if we are away."""
#        return False

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return self._eco_temperature

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return self._comfort_temperature

#    @property
#    def device_state_attributes(self):
#        """Return the device specific state attributes."""
#        dev_specific = {
#            ATTR_STATE_LOCKED: self._thermostat.locked,
#            ATTR_STATE_LOW_BAT: self._thermostat.low_battery,
#            ATTR_STATE_VALVE: self._thermostat.valve_state,
#            ATTR_STATE_WINDOW_OPEN: self._thermostat.window_open,
#            ATTR_STATE_AWAY_END: self._thermostat.away_end,
#        }
#
#        return dev_specific

    def update(self):
        """Update the data from the thermostat."""
        try:
            self._temperature = self._device.get_temperature()
            self._target_temperature = self._device.get_soll_temperature()
            self._comfort_temperature = self._device.get_komfort_temperature()
            self._eco_temperature = self._device.get_absenk_temperature()
            _LOGGER.warning("update")
        except Exception as e:
            _LOGGER.warning("Updating the state failed: %s", e)
