mktime argument out of range when logging in to Crunchyroll after --crunchyroll-purge-credentials
<!--
Thanks for reporting a plugin issue!
USE THE TEMPLATE. Otherwise your plugin issue may be rejected.

First, see the contribution guidelines:
https://github.com/streamlink/streamlink/blob/master/CONTRIBUTING.md#contributing-to-streamlink

Also check the list of open and closed plugin issues:
https://github.com/streamlink/streamlink/issues?q=is%3Aissue+label%3A%22plugin+issue%22

Please see the text preview to avoid unnecessary formatting errors.
-->


## Plugin Issue

<!-- Replace the space character between the square brackets with an x in order to check the boxes -->
- [x] This is a plugin issue and I have read the contribution guidelines.
- [x] I am using the latest development version from the master branch.


### Description

Whenver I try to log in to Crunchyroll via streamlink I get an error.
<!-- Explain the plugin issue as thoroughly as you can. -->


### Reproduction steps / Explicit stream URLs to test

<!-- How can we reproduce this? Please note the exact steps below using the list format supplied. If you need more steps please add them. -->

1. I enter the command streamlink --crunchyroll-username=xxxx --crunchyroll-password=yyy --crunchyroll-purge-credentials https://www.crunchyroll.com/my/episode/to/watch best and I get it every time

### Log output

<!--
TEXT LOG OUTPUT IS REQUIRED for a plugin issue!
Use the `--loglevel debug` parameter and avoid using parameters which suppress log output.
https://streamlink.github.io/cli.html#cmdoption-l

Make sure to **remove usernames and passwords**
You can copy the output to https://gist.github.com/ or paste it below.

Don't post screenshots of the log output and instead copy the text from your terminal application.
-->

```
[cli][debug] OS:         Windows 10
[cli][debug] Python:     3.6.6
[cli][debug] Streamlink: 1.7.0
[cli][debug] Requests(2.24.0), Socks(1.7.1), Websocket(0.57.0)
[cli][info] Found matching plugin crunchyroll for URL https://www.crunchyroll.com/jujutsu-kaisen/episode-10-idle-transfiguration-797874
[cli][debug] Plugin specific arguments:
[cli][debug]  --crunchyroll-username=kashiman290@gmail.com (username)
[cli][debug]  --crunchyroll-password=******** (password)
[cli][debug]  --crunchyroll-purge-credentials=True (purge_credentials)
[utils.l10n][debug] Language code: en_US
[plugin.crunchyroll][debug] Creating session with locale: en_US
[plugin.crunchyroll][debug] Session created with ID: 576c3d5d7a83d1dd18217343a6df37ff
[plugin.crunchyroll][debug] Attempting to login using username and password
[plugin.crunchyroll][debug] Credentials expire at: 1969-12-31 08:00:00
Traceback (most recent call last):
  File "runpy.py", line 193, in _run_module_as_main
  File "runpy.py", line 85, in _run_code
  File "C:\Program Files (x86)\Streamlink\bin\streamlink.exe\__main__.py", line 18, in <module>
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink_cli\main.py", line 1029, in main
    handle_url()
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink_cli\main.py", line 585, in handle_url
    streams = fetch_streams(plugin)
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink_cli\main.py", line 465, in fetch_streams
    sorting_excludes=args.stream_sorting_excludes)
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink\plugin\plugin.py", line 317, in streams
    ostreams = self._get_streams()
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink\plugins\crunchyroll.py", line 312, in _get_streams
    api = self._create_api()
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink\plugins\crunchyroll.py", line 384, in _create_api
    login = api.authenticate()
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink\plugins\crunchyroll.py", line 225, in authenticate
    self.cache.set("auth", self.auth, expires_at=data["expires"])
  File "C:\Program Files (x86)\Streamlink\pkgs\streamlink\cache.py", line 75, in set
    expires = mktime(expires_at.timetuple())
OverflowError: mktime argument out of range
```


### Additional comments, etc.



[Love Streamlink? Please consider supporting our collective. Thanks!](https://opencollective.com/streamlink/donate)
