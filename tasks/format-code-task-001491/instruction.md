"auto" mode shows Heat/Cool in UI because of incorrect mapping in climate smartthings
### The problem

The mapping for "auto" mode is set to HVACMode.HEAT_COOL while it should be set to HVACMode.AUTO.
Setting this to auto makes the UI display it correctly. Functionality wise no issue but it displays wrong state in UI because of incorrect mapping. It might break others but for my samsung AC (2025 windfree) it is the case.

### What version of Home Assistant Core has the issue?

core-2025.4.0

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

smartthings

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/smartthings/

### Diagnostics information

[home-assistant_smartthings_2025-04-03T20-36-36.120Z.log](https://github.com/user-attachments/files/19594357/home-assistant_smartthings_2025-04-03T20-36-36.120Z.log)

### Example YAML snippet

```yaml

```

### Anything in the logs that might be useful for us?

```txt
2025-04-03 20:36:19.450 DEBUG (MainThread) [pysmartthings] Received event: {"eventTime":1743712579353,"eventType":"DEVICE_EVENT","deviceEvent":{"eventId":"4c550136-10cb-11f0-9492-09f246caf6de","locationId":"4385955f-a398-4474-b0e9-a47cb6affe3d","ownerId":"4385955f-a398-4474-b0e9-a47cb6affe3d","ownerType":"LOCATION","deviceId":"5190ecad-d098-7ffa-3b7a-bcc335b0689c","componentId":"main","capability":"airConditionerMode","attribute":"airConditionerMode","value":"auto","valueType":"string","stateChange":true,"data":{},"subscriptionName":"My Home Assistant sub","commandId":"","sensitive":false}}
```

### Additional information

UI shows state as Heat/Cool as the mapping for "auto" is set to HVACMode.HEAT_COOL.
Setting the mapping to HVACMode.AUTO seems to fix it for me.
It can be a breaking change for others but for me the above is the case.
