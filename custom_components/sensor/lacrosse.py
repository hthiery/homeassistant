"""
Support for LaCrosse sensor components.
"""
import logging
import pylacrosse

import voluptuous as vol

from homeassistant.components.sensor import ENTITY_ID_FORMAT
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    ATTR_FRIENDLY_NAME, EVENT_HOMEASSISTANT_STOP, CONF_DEVICE, CONF_SENSORS,
    STATE_UNKNOWN, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity, async_generate_entity_id

REQUIREMENTS = ['pylacrosse']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'lacrosse'

CONF_BAUD = 'baud'
CONF_TYPE = 'type'
CONF_ID = 'id'

DEFAULT_DEVICE = '/dev/ttyUSB0'
DEFAULT_BAUD = '57600'

TYPES = ['humidity', 'temperature']

SENSOR_SCHEMA = vol.Schema({
    vol.Required(CONF_TYPE): vol.In(TYPES),
    vol.Required(CONF_ID): cv.positive_int
})

#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Required(CONF_TYPE): vol.In(TYPES),
#    vol.Required(CONF_ID): cv.positive_int
#})

lacrosse = None

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the LaCrosse component."""

    from serial import Serial

    usb_device = config.get(CONF_DEVICE, DEFAULT_DEVICE)
    baud = int(config.get(CONF_BAUD, DEFAULT_BAUD))
    _LOGGER.debug("%s %s" % (usb_device, baud))
    try:
        lacrosse = pylacrosse.LaCrosse(usb_device, baud)
        lacrosse.open()
    except SerialExecption as e:
        _LOGGER.exception("Unable to open serial port for LaCrosse: %s", e)
        return False

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, close_serial_port)

    sensors = []
    for device, device_config in config[CONF_SENSORS].items():
        _LOGGER.debug("%s %s" % (device, device_config))

        typ = device_config.get(CONF_TYPE)
        try:
            sensor_class = TYPE_CLASSES[typ]
        except KeyError:
            _LOGGER.exception("Unknown LaCrosse sensor type: %s", typ)

        friendly_name = device_config.get(ATTR_FRIENDLY_NAME, device)

        sensors.append(
            sensor_class(
                hass,
                lacrosse,
                device,
                friendly_name,
                device_config
            )
        ) 

    if not sensors:
        _LOGGER.error("No sensors added")
        return False

    add_devices(sensors)


def close_serial_port(*args):
    """Close the serial port uesed for the lacrosse."""
    lacrosse.close()


class LaCrosse(Entity):

    _temperature = None
    _humidity = None
    _low_battery = None

    def __init__(self, hass, lacrosse, device_id, friendly_name, config):
        self.hass = hass
        self.entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, device_id,   
                                                      hass=hass)
        self._config = config 
        self._name = friendly_name 
        self._value = STATE_UNKNOWN

        lacrosse.register_callback(self._config["id"], self._callback)

    @property
    def name(self):
        """Return the name of the sensor."""                                     
        return self._name


    def update(self, *args):
        """Get the latest data."""
        pass

    @property                                                                    
    def device_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        low_battery = self._low_battery
        if low_battery is not None:
            attributes['low_battery'] = low_battery

    def _callback(self, lacrosse_sensor):
        self._temperature = lacrosse_sensor.temperature
        self._humidity = lacrosse_sensor.humidity
        self._low_battery = lacrosse_sensor.low_battery


class LaCrosseTemperature(LaCrosse):

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def state(self):
        """Return the state of the sensor."""                                     
        return self._temperature


class LaCrosseHumidity(LaCrosse):

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return '%' 

    @property
    def state(self):
        """Return the state of the sensor."""                                     
        return self._humidity


TYPE_CLASSES = {                                                                 
    "temperature": LaCrosseTemperature,
    "humidity": LaCrosseHumidity
}
