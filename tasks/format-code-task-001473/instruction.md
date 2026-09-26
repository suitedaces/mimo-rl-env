I want every WAAX plug-in instance, such as an object returned by `WX.Fader()` or another registered generator, processor, or analyzer factory, to expose a common stateful control surface for routing, parameters, and presets.

A plug-in instance should support `to(target)`, where `target` may be another WAAX plug-in with an audio input or a native Web Audio `AudioNode`; it should connect the instance's output to that target and return the target so patching can be chained. Calling `cut()` on the instance should disconnect all outgoing connections from that plug-in.

The instance should support `set(param, arg)` and `get(param)`. For a single value, `set('input', 0.25)` should immediately update that parameter at the current audio context time and return the same plug-in instance for chaining; a later `get('input')` should return `0.25`. For an automation envelope, `set('gain', [[0.0], [1.0, 0.01, 1], [0.0, 0.5, 2]])` should apply each envelope point to the named parameter in order, passing through each point's value, time, and ramp type. Setting an unknown parameter should be a no-op that still returns the same instance, and getting an unknown parameter should return `null`.

The instance should support `setPreset(preset)` and `getPreset()`. Calling `setPreset({ input: 0.5, output: 0.75 })` should immediately apply each listed parameter at the current audio context time. Calling `getPreset()` should return a plain object snapshot of the instance's current parameter values, so after setting those values the snapshot includes `input: 0.5` and `output: 0.75`.

If `to(target)` receives something that cannot be patched as a plug-in or Web Audio node, it should report a WAAX connection error instead of silently succeeding.
