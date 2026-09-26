SQLite version 3.31.1 is not supported, although this is the official version of Ubuntu 20.04.3 LTS
### The problem

I have Ubuntu 20.04.3 LTS, and in HA logs I saw
"2021-11-03 22:34:07 WARNING (Recorder) [homeassistant.components.recorder.util] Version 3.31.1 of SQLite is not supported; minimum supported version is 3.32.1. Starting with Home Assistant 2022.2 this will prevent the recorder from starting. Please upgrade your database software before then"

I try to update to update SQLite,
sudo apt-get install libsqlite3-dev
and it is newest version
"libsqlite3-dev is already the newest version (3.31.1-4ubuntu0.2)"

It would be great if HA could work with at least those versions that can be updated in LTS operating systems, since building new versions from sources is not quite the right approach



### What version of Home Assistant Core has the issue?

	core-2021.11.0

### What was the last working version of Home Assistant Core?

2021.10.0

### What type of installation are you running?

Home Assistant Core

### Integration causing the issue

recorder

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/recorder

### Example YAML snippet

_No response_

### Anything in the logs that might be useful for us?

```txt
2021-11-03 22:34:07 WARNING (Recorder) [homeassistant.components.recorder.util] Version 3.31.1 of SQLite is not supported; minimum supported version is 3.32.1. Starting with Home Assistant 2022.2 this will prevent the recorder from starting. Please upgrade your database software before then
```


### Additional information



Version | core-2021.11.0
-- | --
Installation Type | Home Assistant Container
Development | false
Supervisor | false
Docker | true
Virtual Environment | true
Python Version | 3.9.0
Operating System Family | Linux
Operating System Version | 5.4.83-v7+
CPU Architecture | armv7l
Timezone | Europe/Moscow
