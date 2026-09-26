## Cannot edit climate device actions when the referenced entity isn't loaded

I have an automation that contains a few "set HVAC mode" / "set preset mode" device actions pointing at one of my thermostats (a climate entity). It works fine while everything is loaded.

The trouble starts when that climate entity is temporarily not present in the running instance — for example I disabled the integration while debugging something, or the entity is otherwise not added yet at startup, even though it's still in the entity registry and my automation still references it by entity_id.

When I open that automation in the UI to tweak something else, two things go wrong:

1. The HVAC-related device actions for that device sometimes don't show up at all in the device actions list, even though the entity is known to the registry and my automation already uses it.

2. If I try to edit one of the existing `set_hvac_mode` actions, the "HVAC mode" dropdown is empty, so I can't pick anything and the editor won't let me save the action. Same story for `set_preset_mode` — the preset dropdown is empty. I'm not trying to change the entity, I just want to adjust the mode value (or just look at / re-save what's already there), but the form is unusable.

So effectively, as soon as the underlying climate entity isn't currently loaded, any automation referencing it via a climate device action becomes uneditable in the UI, even though Home Assistant clearly still knows the entity exists.

I'd expect the device action editor to still work in this situation:

- The HVAC mode / preset mode device actions for a known climate entity should remain visible / listable, not vanish just because the entity isn't currently providing a live state.
- The dropdowns for HVAC mode and preset mode should still be populated with the entity's supported modes, so I can actually edit and save the automation. The information about which modes the entity supports is already known to Home Assistant — it shouldn't only be reachable via a live state.

This is pretty painful because any time an integration is briefly unavailable, all the automations referring to its climate entities become read-only in the UI.
