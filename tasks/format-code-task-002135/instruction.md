## Working with RGB(A) imagery is rough around the edges

I've been trying to do a pretty plain RGB workflow with datacube — read a 3-band GeoTIFF, peek at its geo info, do a tiny bit of processing, then write it back out as a COG — and I hit friction at every step. They all feel like the same underlying gap (RGB / RGBA imagery has an extra channel axis and nothing in the API treats it as a first-class case), so filing it as one report.

### 1. `rio_slurp_xarray` returns band-first

```python
da = rio_slurp_xarray('rgb.tif')
da.shape       # (3, H, W)
da.dims        # band axis first
```

This is how rasterio reads multi-band data, but for a 3- or 4-channel image (y, x, band) is what every imaging library I'd want to chain into expects — `matplotlib.imshow`, skimage, PIL, etc. So I end up sticking a transpose at every call site. Could the helper recognise the common RGB / RGBA case and hand me back image-shaped data by default?

### 2. `.geobox` on an image-shaped DataArray

If I take an RGB DataArray with axes laid out as (y, x, band) (either by transposing the result of (1), or by constructing one myself), accessing `.geobox` doesn't do the right thing — it seems to assume the last two axes are the spatial ones, so it ends up treating the channel axis as one of the spatial axes and either errors out or returns nonsense. I'd expect `.geobox` to find the actual y/x dims regardless of where the channel axis sits.

### 3. `write_cog` only accepts band-first 3D arrays

Symmetrically, on the write side:

```python
write_cog(rgb_yxc, 'out.tif')   # rgb_yxc has shape (H, W, 3)
```

doesn't work — `write_cog` treats a 3D array strictly as (band, y, x), so passing it the image-natural (y, x, band) layout either blows up on the shape check or writes garbled output. Same comment as (1): (y, x, band) is what comes out of most imaging pipelines, so it'd be great if `write_cog` accepted that layout too and figured out the right thing to write.

---

Could datacube handle RGB(A) imagery a bit more gracefully across these three spots? Happy to test against a sample image if useful.
