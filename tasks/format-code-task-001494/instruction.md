<!-- READ THIS FIRST:
- If you need additional help with this template please refer to https://www.home-assistant.io/help/reporting_issues/
- Make sure you are running the latest version of Home Assistant before reporting an issue: https://github.com/home-assistant/home-assistant/releases
- Frontend issues should be submitted to the home-assistant-polymer repository: https://github.com/home-assistant/home-assistant-polymer/issues
- iOS issues should be submitted to the home-assistant-iOS repository: https://github.com/home-assistant/home-assistant-iOS/issues
- Do not report issues for components if you are using custom components: files in <config-dir>/custom_components
- This is for bugs only. Feature and enhancement requests should go in our community forum: https://community.home-assistant.io/c/feature-requests
- Provide as many details as possible. Paste logs, configuration sample and code into the backticks. Do not delete any text from this template!
-->

**Home Assistant release with the issue:**
<!--
- Frontend -> Developer tools -> Info
- Or use this command: hass --version
-->

0.94.1

**Last working Home Assistant release (if known):**

unknown

**Operating environment (Hass.io/Docker/Windows/etc.):**
<!--
Please provide details about your environment.
-->

arch | x86_64
dev | false
docker | true
hassio | false
os_name | Linux
python_version | 3.7.3
timezone | America/Chicago
version | 0.94.1
virtualenv | false

**Component/platform:**
<!--
Please add the link to the documentation at https://www.home-assistant.io/components/ of the component/platform in question.
-->

alexa/smart_home

**Description of problem:**

These errors are repeated several times. DEBUG is turned on, however, no relevant debug information is produced.

```
2019-06-08 07:58:46 ERROR (MainThread) [homeassistant.core] Error doing job: Task exception was never retrieved
Traceback (most recent call last):
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 1124, in async_entity_state_listener
    alexa_changed_entity)
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 1418, in async_send_changereport_message
    properties = list(alexa_entity.serialize_properties())
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 312, in serialize_properties
    for prop in interface.serialize_properties():
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 388, in serialize_properties
    prop_value = self.get_property(prop_name)
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 683, in get_property
    'value': float(temp),
TypeError: float() argument must be a string or a number, not 'NoneType'
2019-06-08 07:58:46 ERROR (MainThread) [homeassistant.core] Error doing job: Task exception was never retrieved
Traceback (most recent call last):
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 1124, in async_entity_state_listener
    alexa_changed_entity)
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 1418, in async_send_changereport_message
    properties = list(alexa_entity.serialize_properties())
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 312, in serialize_properties
    for prop in interface.serialize_properties():
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 388, in serialize_properties
    prop_value = self.get_property(prop_name)
  File "/usr/src/app/homeassistant/components/alexa/smart_home.py", line 683, in get_property
    'value': float(temp),
ValueError: could not convert string to float: 'unknown'
```

**Problem-relevant `configuration.yaml` entries and (fill out even if it seems unimportant):**
```yaml
alexa:
  smart_home:
    endpoint: "https://api.amazonalexa.com/v3/events"
    client_id: !secret alexa_sh_client_id
    client_secret: !secret alexa_sh_client_secret
    filter:
      include_domains:
        - switch
        - light
        - fan
        - vacuum
        - lock
      exclude_entities:
        - switch.coffee_maker
        - switch.coyote_wifi
        - switch.coyote_wired
        - switch.daniel_heat_mode
        - switch.kitchen_kettle
        - switch.living_media
        - switch.office_heat_mode
        - switch.office_printer
        - switch.washer
        - switch.zigbee2mqtt_join
        - light.dog_status
        - light.office_status
        - light.art_over_1
        - light.art_over_2
        - light.art_over_3
        - light.art_over_4
        - light.celestebed_floorlamp_left
        - light.celestebed_floorlamp_middle
        - light.celestebed_floorlamp_right
        - light.celestebed_floorlamp_top
        - switch.dance_tv_ir
        - light.daniel
        - light.dining_room
        - light.dishwasher_status
        - light.front_over_1
        - light.front_over_2
        - light.front_over_3
        - light.grp1
        - light.grp2
        - light.grp3
        - light.grp4
        - light.hall
        - light.living_room
        - light.hue_white_lamp_1
        - light.ibox001
        - light.office
        - light.office_vent
        - light.sidehall_status
      include_entities:
        - climate.house_cool_occupied
        - climate.house_heat_occupied
        - climate.danielbed_heat
        - sensor.hvac_temperature
        - sensor.danielbed_temperature_adj
        - sensor.front_temperature_adj
        - sensor.office_temperature_adj
        - sensor.art_temperature_adj
        - sensor.living_temperature_adj
        - sensor.kitchen_temperature_adj
        - sensor.nook_temperature_adj
        - sensor.guestbed_temperature_adj
        - sensor.celestebed_temperature_adj
        - sensor.masterbath_temperature_adj
        - sensor.garage_big_door_temperature_measurement
        - input_boolean.guest
        - media_player.office_speaker
    entity_config:
      switch.back_patio:
        display_categories: LIGHT
      switch.celestebed_lavalamp:
        display_categories: LIGHT
      switch.celestebed_overlight:
        display_categories: LIGHT
      switch.celestebed_underlight:
        display_categories: LIGHT
      switch.kitchen_overhead:
        display_categories: LIGHT
      switch.kitchen_oversink:
        display_categories: LIGHT
      switch.kitchen_under:
        display_categories: LIGHT
      switch.mainhall_front_overhead:
        display_categories: LIGHT
      switch.masterbath_overhead:
        display_categories: LIGHT
      switch.masterbath_exhaustfan:
        display_categories: FAN
      switch.outletu004_usb:
        display_categories: LIGHT
      switch.celestebed_fan:
        display_categories: FAN
      switch.living_fan:
        display_categories: FAN
```

**Traceback (if applicable):**
```

```

**Additional information:**
