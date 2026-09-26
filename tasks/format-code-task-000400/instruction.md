# Share the resize-hotspot construction logic across header cells

Every header cell (row, column, corner, frozen column…) draws an invisible "resize
hotspot" — a thin rectangle the user can grab to drag-resize a row height or a column
width. Today each cell type builds that rectangle's canvas attributes by hand, copying
the same block of literals (fill, opacity, cursor, the `appendInfo` metadata the
interaction layer reads back when a drag starts). The copies have already drifted apart,
which makes resize bugs easy to introduce and hard to fix in one place.

Please extract this into a small, reusable interaction utility so that building a resize
hotspot — and getting the foreground group the hotspots live in — is done the same way
everywhere.

Expose it as a resize interaction utility module importable at
`@/utils/interaction/resize`, providing two named functions: `getResizeAreaAttrs` (the
hotspot attribute builder) and `getResizeAreaGroupById` (the group lookup). How you
structure the internals is up to you.

## What to provide

**1. Build the hotspot rectangle attributes from a single config.**

Given a config describing one hotspot, produce the attribute object that gets handed to
the canvas `addShape('rect', { attrs })` call. The config carries:

- `type` — `'row'` for a row-height hotspot, `'col'` for a column-width hotspot.
- `effect` — what the drag changes: `'field'`, `'cell'` or `'tree'`.
- `theme` — the resize-area style, with at least `size`, `background` and
  `backgroundOpacity`.
- `offsetX`, `offsetY`, `width`, `height` — the geometry of the *cell* the hotspot
  belongs to (used later to compute the drag delta and guide-line position).
- optional `id` (the field id) and `caption` (the dimension value).

The returned attributes must be:

- `fill` set to the theme background, and `fillOpacity` to the theme background opacity.
- `cursor` set to `"<type>-resize"` (so `'col-resize'` / `'row-resize'`).
- `width` and `height` describing only the *thickness* of the hotspot, leaving the other
  dimension for the caller to fill in: a `'col'` hotspot is a vertical bar, so its
  `width` is the theme `size` and its `height` is `null`; a `'row'` hotspot is a
  horizontal bar, so its `height` is the theme `size` and its `width` is `null`.
- an `appendInfo` object that the interaction layer can later read off the shape to drive
  the resize. It must flag the shape as a resize hotspot, and carry the `type`, `effect`,
  `id`, `caption` (when given), `offsetX`, `offsetY`, and the cell `width`/`height` from
  the config. The `theme` must not be copied into `appendInfo`.

Note the deliberate split: the top-level `width`/`height` are the rendered bar's
thickness, while the `width`/`height` inside `appendInfo` are the original cell
dimensions.

**2. Get (or lazily create) a named resize-area group.**

Resize hotspots of a kind share one group under the sheet's foreground group, looked up
by a fixed id. Provide a helper that, given the sheet and a group id, returns that group:
the already-existing child group with that id if there is one, otherwise a freshly added
group registered under that id. Calling it repeatedly with the same id must never create
duplicate groups. If the sheet has no foreground group yet, it should return nothing
rather than throw.
