# Improve how linestrings are assigned to their covering polygon

When OSMNames builds the place hierarchy, every feature is assigned a `parent_id`
pointing at the single polygon that "covers" it (the most specific administrative
area it sits in). For polygons, points and housenumbers this works well, but for
**linestrings** (streets, rivers, …) the current rule is too strict and leaves many
of them without a parent.

Today a linestring only receives a parent when a polygon **fully contains the entire
linestring**, and only when that polygon is fine-grained enough (its `place_rank` is
at or above a fixed threshold). In practice streets routinely run right up to — or
across — an administrative boundary, or poke slightly outside the area they belong to,
so full containment almost never holds and the linestring is left unparented. The
`place_rank` gate makes this worse by ignoring coarser polygons entirely.

Change the way the single-covering-polygon assignment decides whether a linestring
belongs to a polygon so it is based on the linestring's **center point** — the point
located halfway along the linestring — rather than on the whole geometry:

- A linestring is assigned to a polygon when that linestring's center point lies
  inside the polygon, **even if the polygon does not contain the rest of the
  linestring** (e.g. the linestring extends beyond the polygon's boundary).
- This must work **regardless of the polygon's `place_rank`** — the previous
  `place_rank` restriction for linestrings is removed; a coarse polygon may become a
  linestring's parent if it contains the center point.
- A linestring whose center point is **not** inside a polygon must **not** be parented
  to it, even if one of its endpoints touches or lies within the polygon.
- When more than one candidate polygon contains the center point, the linestring is
  assigned to the most specific one (the smallest, highest-`place_rank` polygon),
  exactly as a single covering polygon is chosen for any other feature.

This change applies to linestrings only. Polygons, points and housenumbers must keep
being assigned to the polygon that fully contains them, exactly as before.
