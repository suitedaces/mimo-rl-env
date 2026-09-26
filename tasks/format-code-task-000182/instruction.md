## Housenumbers near administrative boundaries don't get a street_id

When I import an OSM extract that spans several adjoining administrative
areas, a lot of housenumbers end up with `street_id IS NULL` after the
import finishes — even though the corresponding street is clearly there in
`osm_linestring`.

Looking at the cases that fail, they all seem to sit close to the boundary
between two parents: the housenumber is tagged into one admin area and the
street geometry it actually belongs to is in the neighbouring one. So the
`parent_id` on the housenumber and on the street differ, and the name-based
matching step (full match / levenshtein / substring) skips them entirely.

Concretely, if I pick one such housenumber and check the linestring with
the matching `normalized_name` a few hundred meters away, it's obviously
the right street — same name, runs right past the address — but they have
different parents, so nothing gets linked. The result is a noticeable gap
in `street_id` coverage along every admin border in the dataset.

I'd expect the name-based street matching to also pick up streets that are
geographically close to the housenumber, not only ones that happen to share
the exact same `parent_id`. Streets near boundaries shouldn't fall through
the cracks just because OSM put them on the "other side" of an admin
polygon.
