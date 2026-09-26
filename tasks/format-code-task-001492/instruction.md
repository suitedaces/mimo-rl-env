HDDTEMP Integration is Deprecated but is still useful.
### The problem

Hddtemp is planned to be deprecated with a deprecation notice showing in 2025.6.0. The notice says it can only be run in systems with a deprecated architecture, but I don't think this is correct.

I run homeassistant operating system and the integration connects fine over the network to hddtemp installed on another server (64 bit fedora IOT 42, not that this matters much).

In addition, the documentation is incorrect- it's perfectly possible to use this integration in a container when connecting to an external hddtemp instance.

### What version of Home Assistant Core has the issue?

core-2025.6.0

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

hddtemp

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/hddtemp/

### Diagnostics information

_No response_

### Example YAML snippet

```yaml
sensor:
  - name: thuban-hddtemp
    platform: hddtemp
    host: 10.6.0.12
    disks:
      - /dev/sda
      - /dev/sdb
      - /dev/sdc                                                 - /dev/sdd
      - /dev/sde
```

### Anything in the logs that might be useful for us?

```txt

```

### Additional information

_No response_
