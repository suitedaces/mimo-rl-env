services with upper case characters fail to register schema on 2023.7.x
### The problem

after updating to 2023.7.1 my esphome device fails to initialise. 
It is a esp32 with a CO2-sensor. it measures CO2 and registers a HA-service to calibrate the sensor.
esphome version: 2023.6.5

## Debug log

```
Logger: homeassistant.config_entries
Source: core.py:1763
First occurred: 19:35:39 (2 occurrences)
Last logged: 19:35:39

Error setting up entry co2-2 for esphome
Error setting up entry co2-1 for esphome
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/config_entries.py", line 390, in async_setup
    result = await component.async_setup_entry(hass, self)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/components/esphome/__init__.py", line 479, in async_setup_entry
    await _setup_services(hass, entry_data, services)
  File "/usr/src/homeassistant/homeassistant/components/esphome/__init__.py", line 669, in _setup_services
    await _register_service(hass, entry_data, service)
  File "/usr/src/homeassistant/homeassistant/components/esphome/__init__.py", line 636, in _register_service
    async_set_service_schema(hass, DOMAIN, service_name, service_desc)
  File "/usr/src/homeassistant/homeassistant/helpers/service.py", line 687, in async_set_service_schema
    response := hass.services.supports_response(domain, service)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/core.py", line 1763, in supports_response
    if not (handler := self._services[domain][service]):
                       ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'co2_2_Callibrate'
```



### What version of Home Assistant Core has the issue?

core-2023.7.1

### What was the last working version of Home Assistant Core?

2023.7.0

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

esphome

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/esphome/

### Diagnostics information

_No response_

### Example YAML snippet

_No response_

### Anything in the logs that might be useful for us?

_No response_

### Additional information

i use this code in my esp32 source code to register the service function (callibrate) during setup.  
`register_service( &MYCO2::callibrate, "Callibrate");`
