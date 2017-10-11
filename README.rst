HomeAssistant LaCrosse Sensor Component
=======================================

Installation
------------
1. First, copy all the files into the Home Assistant location. It can now be installed either to the custom_components folder 

    /home/homeassistant/.homeassistant/custom_components

or the root folder (using virtual environment)

    /srv/homeassistant/homeassistant_venv/lib/python3.4/site-packages/homeassistant/components

Configuration
-------------

.. code-block:: yaml

    - platform: lacrosse
      sensors:
        wohnzimmer_temperature:
          friendly_name: Wohnzimmer Temperatur
          type: temperature
          id: 60
