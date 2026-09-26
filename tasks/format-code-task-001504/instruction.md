### The problem

A bunch of my Zigbee battery-powered sensors (paired through deCONZ) don't expose any battery state in Home Assistant. In the Phoscon / deCONZ side I can clearly see these devices report a "low battery" flag — they just don't report a full percentage value, only the boolean. As a result HA shows no battery-related entity for them at all, and I can't build an automation that pings me when one of them is running low.

Devices that *do* report an actual percentage already show up fine as a battery sensor in HA, so this only affects the ones that only have the low-battery flag. The tampering flag from deCONZ is surfaced as a binary_sensor on those same devices, so I'd expect something similar for the low-battery state.

### What I'd like

For any deCONZ sensor that reports a low-battery state, Home Assistant should expose an entity reflecting that state, so I can use it in automations the same way I use the existing battery percentage sensors. It should track the underlying value (i.e. flip when the device reports low battery becoming true / false) and not appear at all for devices that don't report the flag.

### Environment

- Home Assistant + deCONZ integration
- Various Zigbee sensors that only report `low_battery` (no percentage), paired through a deCONZ gateway
