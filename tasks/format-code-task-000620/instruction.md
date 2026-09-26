## Session agent doesn't work when snapd snap is installed on core

When the snapd snap is installed on a core system, the session agent it ships isn't picked up by the desktop session.

Looking at what the snapd snap actually provides under `usr/share/applications/`, there are `.desktop` files in there (the SessionAgent one in particular is the reason I noticed this — without its desktop entry the session agent isn't launched). But on the running core system, `/var/lib/snapd/desktop/applications/` doesn't gain those entries after the snapd snap is set up, so the desktop environment never sees them.

This looks inconsistent with how other things shipped by the snapd snap are handled on core. For example the D-Bus session service activation files (also under `usr/share/dbus-1/services/` inside the snap) do get materialized into the corresponding system directory when `AddSnapdSnapServices` runs, and removed again on the undo path. The `.desktop` files coming from the snapd snap don't seem to get the same treatment — they're never written out on install, and (consequently) there's nothing cleaning them up on removal/revert either.

This only affects core; on classic the distro packaging is responsible for those files, so they're already in place there.

Could the snapd-snap-on-core install path be extended so that the desktop files the snapd snap ships are deployed into the system desktop applications directory (and torn down again when the snapd snap is removed / its install is rolled back)? That would let the session agent (and anything else exposed via a desktop entry from the snapd snap) actually function.
