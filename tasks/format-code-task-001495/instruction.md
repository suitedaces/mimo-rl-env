Add scene.apply service
**Home Assistant release with the issue:** 0.99
**Component/platform:** Scene
**Description of problem:**

Home Assistant has a powerful scene engine, but it's very static. Right now you can change scenes, but only in YAML after which you need to reload. We can do better.

This issue is about creating a new `scene.apply` service that will take the definition of a scene as the service parameters and applies it.

Service should be added to [`homeassistant/scene.py`](https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/homeassistant/scene.py)

Example service data (just like the [scene config](https://www.home-assistant.io/components/scene)):

```
light.kitchen: on
light.ceiling:
  state: on
```
