### Works tab is empty for artists that only have collections (no artist series)

On the artist page, the **Works** tab currently renders the artist series rail beneath the top works rail. For artists who don't have any artist series associated with them but who *do* belong to one or more collections, this section just shows up empty — the collections never appear on the Works tab at all.

For comparison, the **Overview** tab shows the collections rail correctly for these same artists. So the data is clearly available; it's just that the Works tab seems to assume every artist will have at least one artist series.

#### Steps to reproduce
1. Find an artist who is featured in at least one collection but has no artist series (we have a few of these in production).
2. Navigate to `/artist/<slug>/works`.
3. Notice that nothing related to series or collections renders in that area — just the top works rail and the artwork filter below.
4. Now navigate to `/artist/<slug>` (Overview). The collections show up fine.

#### Expected
On the Works tab, when an artist has no artist series, we should fall back to showing their collections so the slot isn't wasted (and so users can still discover the artist via collections from this tab). When the artist *does* have artist series, behavior should stay as it is today — show the artist series rail.

The Overview tab should continue to behave as it currently does (collections only — no change there).
