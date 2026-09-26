Drawing of certain paths breaks in `cartopy` 0.25.0
Hello! I’m a developer of [mosaic](https://github.com/e3SM-Project/mosaic), a python package for unstructured mesh visualization which is heavily reliant on cartopy.

We’ve noticed an issue drawing certain paths when switching from cartopy `0.24.0` to `0.25.0`. See [E3SM-Project/mosaic/#42](https://github.com/E3SM-Project/mosaic/issues/42) for the original issue where this was brought to our attention.  Here’s a minimum working example:
```python
import cartopy
import cartopy.crs as ccrs
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import PolyCollection

# https://wktmap.com/?fae129b6
patch = np.array([[
    [-180.00020734,  -63.5383884 ],
    [-179.93611911,  -63.61745971],
    [-179.77001049,  -63.62512738],
    [-179.67109735,  -63.55616224],
    [-179.74190981,  -63.49385818],
    [-179.91362571,  -63.48807984],
    [-180.00020734,  -63.5383884 ],
    [-180.00020734,  -63.5383884 ],
]])

fig, ax = plt.subplots(
    constrained_layout=True, subplot_kw={"projection": ccrs.PlateCarree()}
)

collection = PolyCollection(patch, array=[1.], ec='k', alpha=0.5)

collection.set_transform(ccrs.PlateCarree())

ax.add_collection(collection)
ax.autoscale_view()

ax.set_title(f"cartopy v{cartopy.__version__}")
ax.gridlines(draw_labels=True)

plt.show() 
```
Here's what the patch looks like in cartopy `0.24.0`:
```
conda create -n cartopy_0.24.0 python=3.13 cartopy=0.24.0
```
<img width="651" height="303" alt="Image" src="https://github.com/user-attachments/assets/7b423efe-e0d8-4eb5-94a7-7458ff80dcf1" />

And, here's what the patch looks like in cartopy `0.25.0`:
```
conda create -n cartopy_0.25.0 python=3.13 cartopy=0.25.0
```
<img width="651" height="355" alt="Image" src="https://github.com/user-attachments/assets/099516da-f3a2-405c-b248-da3259bf37b7" />

----

My hunch is that the issue arises because the first/last index lies outside of the projection boundary (i.e. -180 deg). But, I haven't had time to through and test that hunch. 

For some context, in `mosaic` we repeat the first index as the last to ensure the polygons are closed. Because we have variable resolution meshes, the polygons can have variable number of sides. To support ragged array likes this, we further repeat the first/last index as many times as needed to fill in up to the max number of sides.

**cc'ing** @xylar @cbegeman
