"""
Support for AVM Fritz!Box fritzhome sensor devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/sensor.fritzhome/
"""
import logging

from custom_components.fritzhome import (DOMAIN, ATTR_AIN, ATTR_FW_VERSION, ATTR_ID,
    ATTR_MANUFACTURER, ATTR_PRODUCTNAME)
from homeassistant.helpers.entity import Entity

DEPENDENCIES = ['fritzhome']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Fritzhome sensor component."""

    if DOMAIN not in hass.data:
        return False

    device_list = hass.data[DOMAIN]

    sensors = []
    for device in device_list:
        if device.has_powermeter:
            sensors.append(FritzhomePowerMeter(hass, device, config))

    if not sensors:
        _LOGGER.error("No sensors added")
        return False

    add_devices(sensors)


class FritzhomePowerMeter(Entity):
    """Implementation of a Fritzhome power meter sensor."""
    _power_in_watt = None
    _energy = None

    def __init__(self, hass, device, config):
        self.hass = hass
        self._config = config
        self._power = None
        self._device = device

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
        except Exception as exc:
            _LOGGER.warning("Updating the state failed: %s", exc)
            self._power = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._power

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {
            ATTR_AIN: self._device.ain,
            ATTR_FW_VERSION: self._device.fw_version,
            ATTR_ID: self._device.id,
            ATTR_MANUFACTURER: self._device.manufacturer,
            ATTR_PRODUCTNAME: self._device.productname,
        }
        return attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'W'

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return 'mdi:flash'
