## Sorting from the App doesn't apply on an unfiltered view, and leaves indexes behind on the dataset

I'm exploring a dataset in the FiftyOne App and playing with the sort
control. Two behaviors look wrong:

**1. Sort has no effect if I haven't applied any other filters yet.**

If I open the dataset fresh (no tag filter, no field filter, nothing
applied) and pick a field to sort by, the grid doesn't reorder at all —
samples stay in their original order.

If I first apply *any* filter (e.g., match a tag) and then pick the same
sort field, the sort works as expected. So the sort feature itself works,
it just doesn't seem to do anything on its own when nothing else has
modified the view.

**2. Sorting auto-adds indexes to my dataset.**

Once I do get a sort to take effect, I notice my dataset has picked up new
indexes — visible via `dataset.list_indexes()` — on whatever field I just
sorted by. As I try out different sort fields in the App they keep
accumulating.

I'm just browsing interactively. I didn't ask to add an index on every
field I happened to click sort on, and I don't want them stuck on the
dataset afterwards.

### Expected

- Picking a sort field in the App should reorder the grid regardless of
  whether any other filters are applied.
- Sorting from the App shouldn't leave persistent indexes on the dataset.
