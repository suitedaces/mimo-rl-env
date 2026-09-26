## Feature request: add a `mobile_app` webhook command that returns the HA config in one call

I'm working on the mobile app side that talks to Home Assistant via the
`mobile_app` webhook. In a couple of places in the app I need to show the
user some basic information about their HA instance — things like the
location name, the configured time zone, the unit system, the HA version,
and the list of loaded components — and on top of that I want to pick up
the frontend's theme color so the app UI can match the user's HA theme.

Today the `mobile_app` webhook doesn't expose any of this, so to populate
those screens the app has to fall back to two extra HTTP calls outside of
the webhook channel:

1. a call to `/api/config` to get the core configuration of the instance,
2. a call to `/manifest.json` to grab the frontend's theme color.

This is awkward for a few reasons:

- The webhook is the path that's already set up, authenticated, and works
  cleanly through cloudhook for remote instances. The two REST endpoints
  above need their own auth / their own remote exposure, so the app ends
  up juggling more than one transport just to render one settings screen.
- It's two extra round trips on top of the webhook the app is already
  making, which adds noticeable latency on slow mobile connections.
- Conceptually, "give me the basics about this HA instance" feels like
  exactly the kind of thing the `mobile_app` webhook should answer — it
  already has commands like `get_zones` that return instance-level info.

It would be great if the `mobile_app` webhook supported a new command
that returns this information in a single response: the core HA
configuration the mobile app needs to display, plus the frontend theme
color. That way the app can drop the two side calls to `/api/config` and
`/manifest.json` entirely and just use the webhook it's already talking
to.

The new webhook command type I'd expect is something like `get_config`.
