### Dataset sampling has no shuffle / seed control

I'm using lema to fine-tune on a mix of HuggingFace datasets, configured through YAML (`DataParams` / `DatasetSplitParams` / `DatasetParams`). I'm running into two related limitations around sampling.

**1. `sample_count` always gives me the head of the dataset**

When I set `sample_count` on a dataset to take, say, 10k examples from a much larger corpus, I always get the first 10k rows. For most public datasets that's a biased slice (sorted by source / topic / date), so my "subsample" experiments are not representative of the full data.

What I'd like is to be able to ask for a *random* subsample, not just a prefix. Right now there's no way to express that on `DatasetParams` — the only knob is `sample_count`.

This also matters in the oversampling case (when `sample_count` is larger than the dataset): currently the result is just the original data concatenated with itself in order, which is even more obviously not what you want for training.

**2. No way to make sampling / mixing reproducible from config**

`build_dataset` does take a `seed` argument that gets forwarded into `interleave_datasets` for mixing, but there's nowhere in the YAML config to actually set it — it has to be passed in programmatically. So two runs of the same training config can produce different mixes, which makes ablations hard to compare.

Even if I could shuffle before sampling (issue #1), I'd want the same control there: pin a seed in the config and get the same subsample every run; leave it unset and get fresh randomness.

### What I'd like

- A way, on a per-dataset basis in the config, to opt into shuffling the dataset before `sample_count` is applied (default off, so existing configs keep behaving the same).
- A way, on the same per-dataset basis, to pin the randomness used for that shuffle so runs are reproducible.
- A way, at the split level, to pin the randomness used when multiple datasets are mixed together, so I don't have to thread a seed through code to get a reproducible mixture.

All three should be optional; if nothing is set, behavior should match what happens today.
