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

Since homeassistant release 0.58 the component is included.

https://home-assistant.io/components/sensor.lacrosse/


Fritzbox
````````

Configuration
'''''''''''''

.. code-block:: yaml

    fritzbox:
      devices:
        - host: <FRITZBOX#1-IP>
          username: <SMARTHOME#1-USER>
          password: <SMARTHOME#1-PASSWORD>
        - host: <FRITZBOX#2-IP>
          username: <SMARTHOME#2-USER>
          password: <SMARTHOME#2-PASSWORD>
          :
        - host: <FRITZBOX#N-IP>
          username: <SMARTHOME#N-USER>
          password: <SMARTHOME#N-PASSWORD>

    #Not needed any longer
    #climate:
    #  platform: fritzhome

    #Not needed any longer
    #switch:
    #  - platform: fritzhome
