# Add a reusable pan & zoom controller for the plotting views

Our VisPy-based views need a small, self-contained controller that owns the
**pan** (2D translation) and **zoom** (2D scale) state of a scene and keeps any
attached GPU programs in sync. Right now the pan/zoom logic is tangled up inside
the canvas code and there is no plain object we can unit-test or reuse.

Please add a `PanZoom` class, importable as `from phy.plot import PanZoom`,
that implements the following behavior.

## Construction & state

- `PanZoom(pan=(0.0, 0.0), zoom=(1.0, 1.0), zmin=..., zmax=...)`.
- By default the controller starts at the origin (`pan == (0, 0)`) with unit
  zoom (`zoom == (1, 1)`). `zmin`/`zmax` have sensible finite defaults.
- `pan` and `zoom` are readable/writable properties. Each holds a pair of
  values (one per axis); reading either returns a length-2 value. A scalar
  assigned to `zoom` applies to both axes.

## Zoom limits

- `zoom` is always kept within `[zmin, zmax]` per axis: assigning a value
  outside the range clamps it to the nearest bound.
- `zmin` and `zmax` are readable/writable and may never cross: setting `zmin`
  above the current `zmax` leaves `zmin` capped at `zmax`, and setting `zmax`
  below the current `zmin` leaves `zmax` raised to `zmin`.
- Changing either bound immediately re-clamps the current `zoom` so it still
  lies within the new range.

## Coordinate transforms

- `map(coords)` converts data coordinates to scene coordinates, applying pan
  first and then zoom about the origin: a point `(x, y)` maps to
  `(zoom_x * (x + pan_x), zoom_y * (y + pan_y))`.
- `imap(coords)` is the exact inverse of `map`.
- Both accept either a single `(x, y)` point or an array of points shaped
  `(n, 2)`, and return a result of the same shape.

## Interactive updates

- `pan_delta(d)` shifts the current pan by the 2D amount `d`.
- `zoom_delta(d, center=(0.0, 0.0))` applies an incremental zoom. The magnitude
  of the change grows with `|d|`; a positive `d` zooms in (increases zoom) and a
  negative `d` zooms out, with the result clamped to `[zmin, zmax]`. The zoom is
  **centered** at `center` (given in scene coordinates): the data point located
  under `center` before the operation stays under it afterwards — that is,
  `imap(center)` is unchanged by the call.
- `reset()` returns the controller to the identity state (`pan == (0, 0)`,
  `zoom == (1, 1)`).

## GPU program binding

- `add(programs)` registers one program or an iterable of programs with the
  controller. A program is any object supporting item assignment (e.g. a VisPy
  `gloo` program, or a plain dict).
- On registration, and on every subsequent change to pan or zoom (through any
  of the operations above), each registered program receives the current state
  via the uniforms `u_pan` and `u_zoom`, each a length-2 value.
