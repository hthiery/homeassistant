HomeAssistant Custom Component
==============================

Installation
------------
1. First, copy all the files into the Home Assistant location. It can now be installed either to the custom_components folder

.. code-block::

    /home/homeassistant/.homeassistant/custom_components

or the root folder (using virtual environment)

.. code-block::

    /srv/homeassistant/homeassistant_venv/lib/python3.4/site-packages/homeassistant/components

Components
----------

LaCrosse
````````

Configuration
'''''''''''''

.. code-block:: yaml

    - platform: lacrosse
      sensors:
        wohnzimmer_temperature:
          name: Wohnzimmer Temperatur
          type: temperature
          id: 60
        wohnzimmer_humidity:
          name: Wohnzimmer Luftfeuchtigkeit
          type: humidity
          id: 60


Fritzhome
`````````

Configuration
'''''''''''''

.. code-block:: yaml

    fritzhome:
      host: <FRITZBOX-IP>
      username: <SMARTHOME-USER>
      password: <SMARTHOME-PASSWORD>

    climate:
      platform: fritzhome

    switch:
      - platform: fritzhome
