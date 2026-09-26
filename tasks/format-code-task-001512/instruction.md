forked-daapd integration doesn't retry
### The problem

Hello,

i develop the addon [Owntone server](https://github.com/a-marcel/hassio-addon-owntone) for hassio and in general it works together with the hassio core `forked-daapd` integration. Unfortunately the addon needs some time to be ready and the forked-daapd integration try to connect to the owntone server way to early and generate an error during the startup:

```
2021-11-30 22:50:41 ERROR (MainThread) [pyforked_daapd] Can not get http://172.30.33.4:3689/api/config with params None
2021-11-30 22:50:42 ERROR (MainThread) [homeassistant.components.media_player] Error while setting up forked_daapd platform for media_player
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 249, in _async_setup_platform
    await asyncio.shield(task)
  File "/usr/src/homeassistant/homeassistant/components/forked_daapd/media_player.py", line 106, in async_setup_entry
    await forked_daapd_updater.async_init()
  File "/usr/src/homeassistant/homeassistant/components/forked_daapd/media_player.py", line 771, in async_init
    if websocket_port := server_config.get("websocket_port"):
AttributeError: 'NoneType' object has no attribute 'get'
``` 

After this *one try*, this integration never try again to connect and this results in a broken media player. 

The current fix is to restart the core (Supervisor -> System -> Core -> Core restart). After the core is restarted, the integration works as expected.

Is there any possibility to implement a retry into the forked-daapd integration ? 

Thanks a lot

### What version of Home Assistant Core has the issue?

core-2021.11.5

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

forked-daapd

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/forked_daapd/

### Example YAML snippet

_No response_

### Anything in the logs that might be useful for us?

```txt
2021-11-30 22:50:41 ERROR (MainThread) [pyforked_daapd] Can not get http://172.30.33.4:3689/api/config with params None
2021-11-30 22:50:42 ERROR (MainThread) [homeassistant.components.media_player] Error while setting up forked_daapd platform for media_player
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 249, in _async_setup_platform
    await asyncio.shield(task)
  File "/usr/src/homeassistant/homeassistant/components/forked_daapd/media_player.py", line 106, in async_setup_entry
    await forked_daapd_updater.async_init()
  File "/usr/src/homeassistant/homeassistant/components/forked_daapd/media_player.py", line 771, in async_init
    if websocket_port := server_config.get("websocket_port"):
AttributeError: 'NoneType' object has no attribute 'get'
```


### Additional information

_No response_
