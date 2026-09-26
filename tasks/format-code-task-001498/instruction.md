Error in logs from zeroconf
<!-- READ THIS FIRST:
  - If you need additional help with this template, please refer to https://www.home-assistant.io/help/reporting_issues/
  - Make sure you are running the latest version of Home Assistant before reporting an issue: https://github.com/home-assistant/core/releases
  - Do not report issues for integrations if you are using custom components or integrations.
  - Provide as many details as possible. Paste logs, configuration samples and code into the backticks.
  DO NOT DELETE ANY TEXT from this template! Otherwise, your issue may be closed without comment.
-->
## The problem
<!-- 
  Describe the issue you are experiencing here to communicate to the
  maintainers. Tell us what you were trying to do and what happened.
-->
There is an error in the logs from the zeroconf integration

## Environment
<!--
  Provide details about the versions you are using, which helps us to reproduce
  and find the issue quicker. Version information is found in the
  Home Assistant frontend: Developer tools -> Info.
-->

- Home Assistant Core release with the issue: 0.113.0
- Last working Home Assistant Core release (if known): 
- Operating environment (OS/Container/Supervised/Core): Supervised
- Integration causing this issue: zeroconf
- Link to integration documentation on our website: https://www.home-assistant.io/integrations/zeroconf/

## Problem-relevant `configuration.yaml`
<!--
  An example configuration that caused the problem for you. Fill this out even
  if it seems unimportant to you. Please be sure to remove personal information
  like passwords, private URLs and other credentials.
-->

```yaml
zeroconf:
```

## Traceback/Error logs
<!--
  If you come across any trace or error logs, please provide them.
-->

```txt
Exception in thread zeroconf-ServiceBrowser__daap._tcp.local.-_nut._tcp.local.-_viziocast._tcp.local.-_elg._tcp.local.-_plugwise._tcp.local.-_dkapi._tcp.local.-_axis-video._tcp.local.-_spotify-connect._tcp.local.-_printer._tcp.local.-_ipps._tcp.local.-_wled._tcp.local.-_ipp._tcp.local.-_miio._udp.local.-_hap._tcp.local.-_api._udp.local.-_googlecast._tcp.local.-_esphomelib._tcp.local._286:
Traceback (most recent call last):
  File "/usr/local/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/local/lib/python3.8/site-packages/zeroconf/__init__.py", line 1675, in run
    self._service_state_changed.fire(
  File "/usr/local/lib/python3.8/site-packages/zeroconf/__init__.py", line 1433, in fire
    h(**kwargs)
  File "/usr/src/homeassistant/homeassistant/components/zeroconf/__init__.py", line 211, in service_update
    info = info_from_service(service_info)
  File "/usr/src/homeassistant/homeassistant/components/zeroconf/__init__.py", line 313, in info_from_service
    address = service.addresses[0]
IndexError: list index out of range
```

## Additional information
