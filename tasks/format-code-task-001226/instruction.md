## Warn users when picking a non-perceptually-uniform 2D colormap

We ship a bunch of 2D colormaps in the `colormaps` directory that get used by `Volume2D` / `Vertex2D` via the `cmap` argument. Several of the older ones aren't perceptually uniform (the steps in the colormap don't correspond to equal perceptual changes), which can be misleading when interpreting brain maps — small differences in the data look bigger or smaller than they actually are depending on where they fall in the colormap.

The good news is that for most of these older colormaps we now also ship a perceptually-uniform counterpart in the same directory (you can see this by listing the `.png` files under the colormaps dir — there are clear pairs of "old" vs "PU_*" / "*_alpha" versions covering essentially the same color scheme).

The problem is that nothing in pycortex tells the user about this. If someone writes e.g.

```python
import cortex
v = cortex.Volume2D(data1, data2, subject, xfmname, cmap="RdBu_covar", ...)
cortex.quickshow(v)
```

it just renders silently with the non-uniform colormap, and unless the user happens to know that a better drop-in replacement exists in the colormaps folder, they'll keep using the worse one. New users especially have no way of knowing which of the bundled 2D colormaps are the "good" ones.

It would be nice if pycortex nudged the user in this case — when a 2D view is being colormapped with one of the known non-perceptually-uniform colormaps that has a direct perceptually-uniform replacement available, surface a message at render/colormapping time pointing them at the better option. For 2D colormaps that don't have a clear PU equivalent we shouldn't say anything, and the call should otherwise behave exactly as before (no error, no change in output).
