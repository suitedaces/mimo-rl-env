Cloud / Alexa - TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
<!-- READ THIS FIRST:
  - If you need additional help with this template, please refer to https://www.home-assistant.io/help/reporting_issues/
  - Make sure you are running the latest version of Home Assistant before reporting an issue: https://github.com/home-assistant/home-assistant/releases
  - Do not report issues for integrations if you are using custom components or integrations.
  - Provide as many details as possible. Paste logs, configuration samples and code into the backticks.
  DO NOT DELETE ANY TEXT from this template! Otherwise, your issue may be closed without comment.
-->
## The problem
<!-- 
  Describe the issue you are experiencing here to communicate to the
  maintainers. Tell us what you were trying to do and what happened instead.
-->


## Environment
<!--
  Provide details about the versions you are using, which helps us to reproduce
  and find the issue quicker. Version information is found in the
  Home Assistant frontend: Developer tools -> Info.
-->

- Home Assistant release with the issue:  106.4
- Last working Home Assistant release (if known): 
- Operating environment (Hass.io/Docker/Windows/etc.):  Hass.io (docker install on Ubuntu)
- Integration causing this issue: Cloud / Alexa
- Link to integration documentation on our website: 

## Problem-relevant `configuration.yaml`
<!--
  An example configuration that caused the problem for you. Fill this out even
  if it seems unimportant to you. Please be sure to remove personal information
  like passwords, private URLs and other credentials.
-->

```yaml

```

## Traceback/Error logs
<!--
  If you come across any trace or error logs, please provide them.
-->

```txt
2020-03-05 03:39:04 ERROR (Thread-3) [pychromecast.socket_client] [Whole House Audio 1:8009] Error reading from socket.
2020-03-05 03:39:04 WARNING (Thread-3) [pychromecast.socket_client] [Whole House Audio 1:8009] Error communicating with socket, resetting connection
2020-03-05 03:39:04 ERROR (MainThread) [homeassistant.core] Error doing job: Task exception was never retrieved
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/components/alexa/state_report.py", line 46, in async_entity_state_listener
    hass, smart_home_config, alexa_changed_entity
  File "/usr/src/homeassistant/homeassistant/components/alexa/state_report.py", line 79, in async_send_changereport_message
    properties = list(alexa_entity.serialize_properties())
  File "/usr/src/homeassistant/homeassistant/components/alexa/entities.py", line 264, in serialize_properties
    for prop in interface.serialize_properties():
  File "/usr/src/homeassistant/homeassistant/components/alexa/capabilities.py", line 231, in serialize_properties
    prop_value = self.get_property(prop_name)
  File "/usr/src/homeassistant/homeassistant/components/alexa/capabilities.py", line 674, in get_property
    current = math.floor(int(current_level * 100))
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
2020-03-05 03:39:04 INFO (SyncWorker_6) [homeassistant.components.command_line.switch] Running state command: ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /config/ssh/id_rsa_router homeassistant@192.168.1.1 sudo /config/scripts/parentalcontrolschromebk STATUS
2020-03-05 03:39:19 ERROR (MainThread) [homeassistant.core] Error doing job: Task exception was never retrieved
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/components/alexa/state_report.py", line 46, in async_entity_state_listener
    hass, smart_home_config, alexa_changed_entity
  File "/usr/src/homeassistant/homeassistant/components/alexa/state_report.py", line 79, in async_send_changereport_message
    properties = list(alexa_entity.serialize_properties())
  File "/usr/src/homeassistant/homeassistant/components/alexa/entities.py", line 264, in serialize_properties
    for prop in interface.serialize_properties():
  File "/usr/src/homeassistant/homeassistant/components/alexa/capabilities.py", line 231, in serialize_properties
    prop_value = self.get_property(prop_name)
  File "/usr/src/homeassistant/homeassistant/components/alexa/capabilities.py", line 674, in get_property
    current = math.floor(int(current_level * 100))
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

## Additional information
I notice that these errors are coming in batches where several integrations will stop responding all at once, but the Alexa one is always consistent.  The others that are affected tend to be at the same time the Alexa error is occurring.  

I do have a custom integration I wrote, but there was no activity at this time with that integration (see my github here: https://github.com/patmann03/custom_components) and I'm fairly certain (but not positive) that these errors were occurring before I implemented this.  I can remove my custom integration, but its basically a copy of the official homeworks integration with the functions updated.
