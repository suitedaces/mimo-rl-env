Since HA Core 2025.2.0 update, MQTT empty payloads don't work anymore
### The problem

**EDIT:** As @JosephRDawson found out, this seems more a problem of empty payloads, see below. Changing title.

I run an AWTRIX 0.98 display (Ulanzi clock) which is supposed to feed back a screenshot of the display every 10 seconds into my dashboard (content changes every 10s). This suddenly stopped working after the HA Core 2025.2.0 upgrade.

My AWTRIX has a MQTT base topic of `awtrix1`. You are supposed to send an empty payload to `awtrix1/sendscreen`, upon which the clock sends back the current screen content as a JSON payload in the `awtrix1/screen` topic.

I use this method to feed an MQTT sensor for the HACS [AWTRIX Light Display Card](https://github.com/RDG88/lovelace-awtrix-light-display-card), defined in `configuration.yaml`:

```yaml
mqtt:
  sensor:
    - name: "Awtrix1 Screenshot"
      unique_id: "awtrix1_screenshot"
      state_topic: "awtrix1/screen"
      value_template: "1"
      json_attributes_topic: "awtrix1/screen"
      json_attributes_template: "{\"screen\": \"{{ value_json }}\"}"
```

Now here is the interesting part: When I use the MQTT Configuration tools to_manually_ publish an empty payload to `awtrix1/sendscreen` and watch the `awtrix1/screen` topic, I get back the screen content immediately, and the dashboard updates just fine.

**But when I run my automation (triggers every 10s), _nothing is updated_—which worked fine before the HA Core 2025.2.0 update:**

```yaml
alias: Awtrix screenshot
description: Gets a screenshot from Awtrix every 10s.
triggers:
  - seconds: /10
    trigger: time_pattern
conditions: []
actions:
  - data:
      topic: awtrix1/sendscreen
    action: mqtt.publish
mode: single
```

**What has changed? Do we now have some kind of rate limiting or just a bug?**

Since nothing else has changed apart from me doing the HA Core 2025.2.0 upgrade, I think we can exclude:
 
- my HA setup
- the custom lovelace card
- the AWTRIX 0.98 (Ulanzi) display
- my automation code

as the reasons for the sudden malfunction between the latest HA Core 2025.1 and HA Core 2025.2.0.

My HA runs on Proxmox, and I use the official Mosquitto MQTT Broker Add-On v6.5.0.

Home Assistant "About" shows the following:

- Core 2025.2.0
- Supervisor 2025.02.0
- Operating System 14.2
- Frontend 20250205.0


### What version of Home Assistant Core has the issue?

2025.2.0

### What was the last working version of Home Assistant Core?

2025.1.?

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

_No response_

### Link to integration documentation on our website

_No response_

### Diagnostics information

_No response_

### Example YAML snippet

```yaml

```

### Anything in the logs that might be useful for us?

```txt

```

### Additional information

_No response_
