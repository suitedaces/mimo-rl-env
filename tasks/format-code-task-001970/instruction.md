## Feature request: allow `mopidy --config` to accept a directory

I'm packaging Mopidy for a setup where different components (audio, mpd, spotify, http, etc.) each ship their own small `.conf` snippet. I'd like to drop all of them into a single directory, e.g.

```
/etc/mopidy/conf.d/
    00-audio.conf
    10-mpd.conf
    20-spotify.conf
    ...
```

and just point Mopidy at that directory:

```
mopidy --config /etc/mopidy/conf.d
```

Today `--config` only accepts individual files. If I want to load several snippets I have to enumerate every file on the command line and keep that list in sync whenever a snippet is added or removed:

```
mopidy --config /etc/mopidy/conf.d/00-audio.conf:/etc/mopidy/conf.d/10-mpd.conf:/etc/mopidy/conf.d/20-spotify.conf:...
```

This is awkward for distro packaging and for users who want to manage their config as a set of drop-ins.

It would be great if `--config` (and the colon-separated list it already accepts) could also take a directory and pick up the config snippets inside it, with the usual "later overrides earlier" precedence still applying so I can still mix directories and individual files on the same command line.
