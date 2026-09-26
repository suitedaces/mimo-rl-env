Folders submitted via the `/config` REST endpoint don't sync

I'm managing a syncthing instance through its REST API. When I POST a folder configuration to `/config` with only the fields I care about (id, path, devices, ro, etc.) and let the rest be implicit, the folder ends up sitting there doing nothing — files that should sync from a connected device never arrive, no errors in the log, the folder just never makes progress.

If I instead let syncthing write a fresh `config.xml` from scratch (or hand-edit the XML and restart), the same folder syncs fine. So the difference seems to be the path the config takes into the running process, not the folder content itself.

Poking at it a bit, the folders that don't sync have `Copiers`, `Pullers`, `Finishers` all reported as 0 in the running config (because my JSON didn't include them). The folders that do sync have non-zero values there — those came from the XML defaults. So when you go through `/config`, you basically have to know about these internal worker-count fields and supply them explicitly, otherwise the folder is silently broken.

That feels wrong — `/config` should give you a working folder with the same defaults you'd get from a freshly-written `config.xml`. A user shouldn't need to know about copier/puller/finisher counts to submit a folder via the API.

Could the config layer make sure folders end up with sane worker counts regardless of which entry point populated them?
