### The problem

I was setting up a template button under the `template:` integration and tried to combine it with a top-level `trigger:` / `action:` so that pressing the button would do some setup work first. My YAML looked roughly like this:

```yaml
template:
  - trigger:
      - platform: state
        entity_id: sensor.something
    action:
      - service: persistent_notification.create
        data:
          message: "before press"
    button:
      - name: My Template Button
        press:
          - service: light.toggle
            target:
              entity_id: light.kitchen
```

Home Assistant happily accepts this configuration on startup with no warnings or errors, but the button doesn't actually behave the way I'd expect — the `trigger` / `action` portion has no effect on it. Looking at the docs, template buttons don't appear to support trigger-based configuration at all (unlike template sensors / binary sensors), so this combination doesn't really make sense.

### What I'd expect

If I configure a template button alongside keys that aren't supported for that platform (like `trigger` and `action`), the config should be rejected at validation time with a clear message telling me which keys aren't allowed, instead of being silently accepted and leaving me to figure out why my button isn't doing what I wrote.

### Version

Latest dev / 2025.3
