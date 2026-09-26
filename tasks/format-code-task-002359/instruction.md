## `event.waitKeys()` always discards pre-existing keypresses — no way to opt out

I'm running an experiment where I present a stimulus and want to collect the participant's response. In some trials I want to do other work (drawing, logging) between the stimulus onset and the moment I block on the response, but I still want to count a keypress that happened during that interval as a valid response.

The natural way to express this is to let key events accumulate in the buffer during the stimulus, and then call `event.waitKeys(...)` to block until I have a response — falling through immediately if one already arrived.

But `event.waitKeys()` unconditionally clears the keyboard buffer on entry, so anything the participant pressed before the call is silently thrown away:

```python
from psychopy import visual, event, core

win = visual.Window()
# ... show stimulus, do some drawing ...
# Suppose the participant presses a key right here, during the stimulus.
core.wait(0.5)

# This call discards that keypress and then waits for a *new* one.
keys = event.waitKeys(keyList=['left', 'right'])
```

The docstring even states this explicitly ("Implicitly clears keyboard, so any preceding keypresses will be lost.") — but in my use case that's exactly the wrong default behavior for the trial, and I can't override it. `event.getKeys()` doesn't help either, because I do want the blocking-with-timeout semantics of `waitKeys`; I just don't want it to wipe the buffer first.

Would it be possible to make the pre-call buffer flush optional, so that callers who care about keypresses from just before the `waitKeys` call can preserve them? The current (clearing) behavior should remain the default so existing experiments aren't affected.

I'd expect the new opt-out to be exposed as something like a `clearEvents` keyword argument on `event.waitKeys(...)`.
