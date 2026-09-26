get_optics does not work on IOS VSS setup
### Description of Issue/Question

Trying to get optics metrics on iOS virtual Switching System (VSS) setup returns nothing.

Source of the issue:

Command *show interfaces transceiver* does not work on vss mode.

It should be 
```
show interfaces transceiver switch 1
show interfaces transceiver switch 2
```

### Did you follow the steps from https://github.com/napalm-automation/napalm#faq
(Place an ``x`` between the square brackets where applicable)

- [X] Yes
- [] No


### Setup

### napalm version

```
Latest Git
```

### Network operating system version
```
Cisco IOS Software, s6t64 Software (s6t64-ADVENTERPRISEK9-M), Version 15.5(1)SY4, RELEASE SOFTWARE (fc4)
```

### Steps to Reproduce the Issue

### Error Traceback
(Paste the complete traceback of the exception between quotes below)
No trace back
