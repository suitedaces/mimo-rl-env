## NVD JSON feed fetch no longer works — NIST deprecated the 1.0 feed

I'm running the NVD fetch to update my local CVE database, but nothing
comes back anymore — the fetcher fails on every year I try.

Poking around on the NIST side, it looks like they've bumped the NVD CVE
JSON feed to a newer version and the old 1.0 endpoints (the
`.../feeds/json/cve/1.0/nvdcve-1.0-*` URLs this project is hitting) have
been retired. The current downloads page only lists the newer feed format
now.

Could the project be updated to pull from the current NVD JSON feed
instead of the now-gone 1.0 one? Right now there's no way to get a fresh
NVD sync without that.
