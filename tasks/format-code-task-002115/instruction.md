## Cannot set `seg_3d_dtype` in config for `LoadAnnotations3D`

I'm trying to configure the `LoadAnnotations3D` pipeline transform from a config file and want to override the dtype used for loading 3D semantic masks (the `seg_3d_dtype` argument). My segmentation labels fit in a smaller integer type than the default, so I'd like to set it to something like `np.int32` from the config.

In my config I have something along the lines of:

```python
dict(
    type='LoadAnnotations3D',
    with_bbox_3d=True,
    with_label_3d=True,
    with_seg_3d=True,
    seg_3d_dtype=np.int32,
    ...
)
```

This doesn't work — config files don't really have a clean way to pass an actual numpy dtype object through, so there's no way for me to express this choice from the config. The argument currently expects a real `np.dtype`, which makes it basically un-overridable for anyone using mmdet3d the normal way (editing a config rather than constructing the transform in Python).

Could `seg_3d_dtype` be made configurable from a config file? Ideally I'd just like to specify which numpy dtype to use without having to subclass the transform or build it manually in Python.
