## Feature request: target services by floor

Floors are already a concept in Home Assistant — areas can be assigned to a floor in the area registry. It would be really convenient if services could be targeted at a whole floor, the same way you can target an `area_id`, `device_id`, or `entity_id` today.

For example, when going to bed I'd like to turn off everything upstairs in a single call:

```yaml
- service: light.turn_off
  target:
    floor_id: upstairs
```

Right now this isn't accepted — `floor_id` isn't a valid key inside a service `target` block.

The workaround is listing every area on the floor explicitly:

```yaml
- service: light.turn_off
  target:
    area_id:
      - bedroom
      - bathroom
      - hallway_upstairs
      - office
```

…but I have to remember to update this list every time I add or rename an area on that floor, which kind of defeats the point of having organized my home into floors in the first place.

It would be great if `floor_id` worked anywhere `area_id` does in a service target, and was resolved to all the entities belonging to areas on that floor.
