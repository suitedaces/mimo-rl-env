## Old model versions are not cleaned up after a rolling update

I'm running Seldon Core v2 and trying out rolling updates on a model. My setup is roughly:

1. Apply a `Model` (e.g. `iris`) pointing at storage URI `.../iris/v1`.
2. Wait for it to become ready.
3. Re-apply the same `Model` with a new storage URI `.../iris/v2` to roll it forward.

The new version comes up fine and starts serving traffic, but the **old version never goes away**. If I keep rolling the model forward (v2 → v3 → v4 …) the previous versions just accumulate in the scheduler — version cleanup never seems to fire for them. I'd expect that once the new version is fully available and serving, the older one(s) should be cleaned up automatically the way the docs imply.

I can reproduce this with a plain sklearn iris model — nothing fancy in the spec, just `requirements: [sklearn]` and a storage URI pointing at a rolling sample bucket.

---

While poking at this I also noticed something that looks related (same "stale state hangs around" flavour, but on the experiment side):

If I update an existing `Experiment` (change weights, change candidates, etc.), the new config takes effect but it doesn't feel like the previous routing for that experiment is being reset first — re-applying the same experiment a couple of times produces routing behaviour that doesn't match what I'd get from creating it fresh. Creating it fresh from a clean state works as expected.

Both symptoms feel like envoy-side state from the previous version of the object isn't being released before the new state is applied. Could the incremental processor be made to behave correctly across repeated model rollouts and experiment updates?
