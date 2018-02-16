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
      host: <FRITZBOX-IP>
      username: <SMARTHOME-USER>
      password: <SMARTHOME-PASSWORD>

    #Not needed any longer
    #climate:
    #  platform: fritzhome

    #Not needed any longer
    #switch:
    #  - platform: fritzhome
