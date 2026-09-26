NIBE F2040: step size for room sensor set point wrong
### The problem

I have a NIBE F2040 ASHP and SMO20. In #131583 the `47398 - Room sensor set point value heating climate system 1` key was added, allowing me to adjust the heating set point from HA.

However the HA only allows steps of 1 degree, where it should be 0.5 degree (which can be done via the physical panel or uplink web interface).

The relevant part of the diagnostic output is

```json
                {
                  "category": "SMO 20",
                  "parameterId": "47398",
                  "parameterName": "Room sensor set point value heating climate system 1",
                  "parameterUnit": "\u00b0C",
                  "writable": true,
                  "timestamp": "2024-12-11T13:23:12+00:00",
                  "value": 14.5,
                  "strVal": "14.5\u00b0C",
                  "smartHomeCategories": [],
                  "minValue": 50.0,
                  "maxValue": 350.0,
                  "stepValue": 5.0,
                  "enumValues": [],
                  "scaleValue": "0.1",
                  "zoneId": null
                },
```
That is after having set to a .5 value from the uplink web interface.

### What version of Home Assistant Core has the issue?

core-2024.12.2

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

myuplink

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/myuplink

### Diagnostics information

_No response_

### Example YAML snippet

_No response_

### Anything in the logs that might be useful for us?

_No response_

### Additional information

There is a diagnostic file on #131583 let me know if you need a new one.
