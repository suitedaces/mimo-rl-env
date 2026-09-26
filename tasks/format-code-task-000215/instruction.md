## Inverted predictions don't flow cleanly into `SaveImage` / can't switch `collate_fn` in `Invertd`

I'm building a post-transform pipeline for a segmentation model:

```python
post_transforms = Compose([
    Activationsd(keys="pred", sigmoid=True),
    AsDiscreted(keys="pred", threshold_values=True),
    Invertd(
        keys="pred",
        transform=pre_transforms,
        loader=val_loader,
        orig_keys="image",
        ...
    ),
    SaveImaged(keys="pred_inverted", output_dir="./out", ...),
])
```

The pre-transforms apply spatial transforms with different parameters per sample (random crops / spacings), so after inversion each sample has a different shape. With the default `collate_fn` in `Invertd` (no collation), `pred_inverted` ends up as a Python list of per-sample tensors without a batch dim — which makes sense, you can't stack tensors of different shapes back into a batch.

The problem is feeding that list into `SaveImage` / `SaveImaged`. `SaveImage` only knows two modes: `save_batch=True` (input is `[B, C, H, W, ...]`) or `save_batch=False` (input is `[C, H, W, ...]`). A list of channel-first tensors falls through neither, and it just crashes / writes garbage. `SegmentationSaver` does handle the list case internally, but `SaveImaged` (which I'd prefer to use in the dict pipeline) does not — so I end up having to drop out of the `Compose` and use the handler.

Separately, I tried working around this by passing a real collate function to `Invertd` (e.g., `list_data_collate` for the cases where shapes do match) so I'd get a single collated dict back instead of a list of per-sample dicts. That also crashes inside `Invertd.__call__` — it unconditionally does `[post_func(i[orig_key]) for i in inverted]`, which assumes `inverted` is a list of dicts. When the collate function returns a single dict, iterating it like that doesn't do what you'd want.

So really two related asks:

1. `SaveImage` (and `SaveImaged` by extension) should accept a list of channel-first tensors / arrays as input, and save each item with its corresponding meta dict — same idea that's already in `SegmentationSaver`, but lifted into the transform itself so it works inside a `Compose` post-transform pipeline.
2. `Invertd` should respect whatever `collate_fn` the user passes — if it returns a list, behave like today; if it returns a single collated structure, handle that too instead of blowing up.

It would also be good if the docstrings for `Invertd` / `TransformInverter` / `SaveImage` / `SegmentationSaver` made it clear what shape the inverted output actually has (list-of-tensors-without-batch-dim vs. batched tensor), because right now it's pretty easy to assume you're getting a batched tensor back and only find out otherwise at the save step.
