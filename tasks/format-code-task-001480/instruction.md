Restarting frigate full access addon fails due to wrong slug: second dash in addon's name makes trouble
### The problem

To reproduce:
1. Install full access version of frigate
2. Create a simple automation e.g. using the UI just executing the service to restart  the "full access" frigate addon. 
3. Execute this automation

Alternatively just execute the restart service through the developer tools.

Executing the automation/service will fail because the full access version of frigate is named "ccab4aaf-frigate-fa".

Reason: The automation uses a slug "ccab4aaf_frigate-fa", which still contains one '-', which is an invalid char in a slug.
The YAML snippet below features the name of the addon and you can see the issue. This name has not been entered manually but was created once I selected the Frigate addon using the UI.

Workaround could be to rename the addon to something like "ccab4aaf-frigatefa", but I'm afraid of side effects ...

Any other reasonable workaround is appreciated :-)

Actually, am not sure if Home Assistant Core should be able to deal with addons using more than 1 dash or if rather the addon should use a more compliant name.

### What version of Home Assistant Core has the issue?

core-2023.9.0

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

frigate (full access) addon 0.12.1

### Link to integration documentation on our website

https://github.com/blakeblackshear/frigate-hass-addons

### Diagnostics information

_No response_

### Example YAML snippet

```yaml
description: ""
mode: single
trigger: []
condition: []
action:
  - service: hassio.addon_restart
    data:
      addon: ccab4aaf_frigate-fa
```


### Anything in the logs that might be useful for us?

```txt
Logger: homeassistant.helpers.script.websocket_api_script
Source: helpers/script.py:420
First occurred: 11:44:46 (2 occurrences)
Last logged: 11:44:51

websocket_api script: Error executing script. Invalid data for call_service at pos 1: invalid slug ccab4aaf_frigate-fa (try ccab4aaf_frigate_fa) for dictionary value @ data['addon']
```


### Additional information

obviously it does not make sense to rename the slug manually because it needs to match the addon ...
