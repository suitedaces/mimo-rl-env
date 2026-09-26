## Inconsistent ROI support across signal/model methods

I use ROIs all the time when working with EELS spectra and TEM/holography images in a Jupyter notebook — typically I draw a `SpanROI` or `RectangularROI` interactively on a plot and then want to feed it into whatever processing method I need next (background removal, ZLP alignment, integration, image alignment, picking a fit range in a model, etc.).

The problem is that the support for passing a ROI as an argument is really inconsistent across the API.

Some methods take a ROI happily:

```python
s = hs.datasets.example_signals.EDS_TEM_Spectrum()
roi = hs.roi.SpanROI(left=5, right=15)
s.remove_background(signal_range=roi, background_type="Polynomial")   # works
```

But many other methods that conceptually take "the same kind of thing" (a range, or a set of coordinates) only accept a plain tuple and reject a ROI:

```python
# Signal1D / EELS
s_ll.align_zero_loss_peak(signal_range=hs.roi.SpanROI(-10., 10.))     # I want this to work

# Model1D — I'd love to reuse the same SpanROI I drew on the plot
m = s.create_model()
m.set_signal_range(roi)
m.add_signal_range(roi)
m.remove_signal_range(roi)
m.fit_component(g1, signal_range=roi)

# Signal2D
im = hs.signals.Signal2D(np.random.random((10, 30, 30)))
rect = hs.roi.RectangularROI(left=2, right=10, top=0, bottom=5)
im.align2D(roi=rect)
im.estimate_shift2D(roi=rect)
```

Right now, for the methods that don't natively accept a ROI, I have to manually pull the attributes off the ROI and rebuild a tuple every time, e.g. `(rect.left, rect.right, rect.top, rect.bottom)` for `align2D`, `(span.left, span.right)` for the model methods, and so on — different shape per ROI type, easy to get wrong, and pretty ugly when I'm just trying to reuse the same ROI object I already have on screen.

It would be really nice if a ROI could be used in place of the corresponding coordinates/range tuple **anywhere** in the API — so that the same `SpanROI` or `RectangularROI` I drew on the plot can be passed directly to all of these methods uniformly, without me having to remember which methods support ROIs and which don't.

Relatedly, in user code it would be very natural to be able to treat a ROI like the tuple it conceptually represents — e.g. unpack it directly:

```python
roi = hs.roi.RectangularROI(left=0, right=10, top=20, bottom=20.5)
left, right, top, bottom = roi    # currently fails
```

This would cover the common cases (`SpanROI`, `RectangularROI`, `Point1DROI`, `Point2DROI`, `CircleROI`, `Line2DROI`) and make ROIs feel like first-class arguments throughout hyperspy.
