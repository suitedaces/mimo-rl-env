## Allow configuring the admin URL path of the Pi-hole instance

I run my Pi-hole behind a reverse proxy and the admin UI isn't reachable at the default `/admin/` path — I've moved it to a different path prefix (e.g. `/pihole/`) so it fits into the rest of my URL layout. The Pi-hole UI itself works fine at that path.

When I point pihole-exporter at this instance:

```
$ ./pihole_exporter \
    -pihole_protocol https \
    -pihole_hostname myhost.example.com \
    -pihole_password '****'
```

it can't pull any stats. From what I can tell the exporter always hits `…/admin/api.php?…` and `…/admin/index.php?login`, so on my setup it's hitting a path that doesn't exist and never reaches the real Pi-hole API.

There doesn't seem to be any flag or environment variable to tell the exporter what path prefix the admin interface actually lives under — it's hardcoded to `/admin/`. That assumption breaks any deployment where the admin UI has been moved (reverse proxy, sub-path hosting, etc.).

It would be great if the admin path segment were configurable, both via CLI flag and via environment variable, in the same style as the other `pihole_*` options. The default should stay as it is today so existing setups don't have to change anything. And like the other per-instance options (`pihole_protocol`, `pihole_port`, `pihole_password`, …), when monitoring multiple Pi-holes from one exporter it should follow the same "one value for all hosts, or one value per host" rule so I can mix instances that use different admin paths.

The new option I'd expect would be named something like `pihole_admin_context` (with a matching `PIHoleAdminContext` field on the config struct), following the existing `pihole_*` naming convention.
