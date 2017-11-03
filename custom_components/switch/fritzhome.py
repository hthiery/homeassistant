"""
Support for AVM Fritz!Box fritzhome switch devices.

For more details about this component, please refer to the documentation at
http://home-assistant.io/components/switch.fritzhome/
"""
import logging
from custom_components.fritzhome import (DATA_FRITZHOME, ATTR_FW_VERSION,
    ATTR_MANUFACTURER, ATTR_PRODUCTNAME)
from homeassistant.components.switch import (
    SwitchDevice, ENTITY_ID_FORMAT
)
from homeassistant.helpers.entity import generate_entity_id

DEPENDENCIES = ['fritzhome']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Fritzhome switch platform."""

    if DATA_FRITZHOME not in hass.data:
        return False

    fritz = hass.data[DATA_FRITZHOME]
    device_list = fritz.get_devices()

    devices = []
    for device in device_list:
        if device.has_switch:
            devices.append(FritzhomeSwitch(hass, device))

    add_devices(devices)


class FritzhomeSwitch(SwitchDevice):
    """The thermostat class for Fritzhome."""

    def __init__(self, hass, device):
        self._device = device
        self.entity_id = generate_entity_id(ENTITY_ID_FORMAT, device.name,
                                            hass=hass)
        self._state = None

    @property
    def available(self):
        """Return if switch is available."""
        return self._device.present

    @property
    def name(self):
        """Return the name of the device."""
        return self._device.name

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {
            ATTR_FW_VERSION : self._device.fw_version,
            ATTR_MANUFACTURER : self._device.manufacturer,
            ATTR_PRODUCTNAME: self._device.productname,
            ATTR_PRODUCTNAME: self._device.productname,
        }
        return attr

    @property
    def is_on(self):
        return self._device.get_switch_state()

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.set_switch_state_on()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.set_switch_state_off()

    def update(self):
        """Get latest data and states from the device."""
        pass
