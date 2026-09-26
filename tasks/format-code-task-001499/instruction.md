Dyson integration does not expose humidity or air quality (pm25) to homekit
<!-- READ THIS FIRST:
  - If you need additional help with this template, please refer to https://www.home-assistant.io/help/reporting_issues/
  - Make sure you are running the latest version of Home Assistant before reporting an issue: https://github.com/home-assistant/core/releases
  - Do not report issues for integrations if you are using custom components or integrations.
  - Provide as many details as possible. Paste logs, configuration samples and code into the backticks.
  DO NOT DELETE ANY TEXT from this template! Otherwise, your issue may be closed without comment.
-->
## The problem

Dyson integration does not expose humidity or air quality (pm25) to homekit by default
<!-- 
  Describe the issue you are experiencing here to communicate to the
  maintainers. Tell us what you were trying to do and what happened.
-->


## Environment
<!--
  Provide details about the versions you are using, which helps us to reproduce
  and find the issue quicker. Version information is found in the
  Home Assistant frontend: Configuration -> Info.
-->

- Home Assistant Core release with the issue: 2020.12.1
- Last working Home Assistant Core release (if known): 
- Operating environment (OS/Container/Supervised/Core): Mac OSX Catalina 10.15.7
- Integration causing this issue: Dyson
- Link to integration documentation on our website: https://www.home-assistant.io/integrations/dyson/

## Problem-relevant `configuration.yaml`
<!--
  An example configuration that caused the problem for you. Fill this out even
  if it seems unimportant to you. Please be sure to remove personal information
  like passwords, private URLs and other credentials.
-->

```yaml
dyson:
  username: "myusername@domain.com"
  password: "mypassword"
  language: "BE"
  devices:
    - device_id: "VS9-EU-KFAXXXXX"
      device_ip: "192.168.0.10"
```

## Traceback/Error logs
<!--
  If you come across any trace or error logs, please provide them.
-->

```txt

```

## Additional information
The dyson integration works perfectly within the bounds of home assistant, however when also combining it with the homekit integration, only the temperature sensor gets exposed.

From looking at the homekit code, the `device_class` of the sensor must be set to `humidity` and for the air quality to be exposed, `device_class` must be `pm25` or the entity name should contain `pm25`.

I managed to work around the issue by adding the following template sensors:

```yaml
  - platform: template
    sensors:
      living_room_humidity_hk:
        friendly_name: "Living Humidity"
        unit_of_measurement: "%"
        value_template: "{{ states('sensor.living_room_humidity') }}"
        device_class: humidity
  - platform: template
    sensors:
      living_room_pm25_hk:
        friendly_name: "Living PM25"
        value_template: "{{ states('sensor.particulate_matter_2_5') }}"
```
I am not fluent at writing python, nor with home assistant code, so I don't think I'll manage a PR. 
I hope this can be adjusted in a next version of HA.
