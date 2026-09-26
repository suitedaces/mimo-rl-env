## Marketo incremental sync fails when records contain null cursor values

I'm using the Marketo source connector to do incremental syncs of a few streams (programs, activities, etc.). For most of the records this works fine, but the sync blows up partway through when it hits records where the cursor field (e.g. `createdAt` / `updatedAt`) comes back as `null` from the Marketo API.

It seems Marketo can legitimately return records with a null timestamp for the cursor field — not a missing key, but explicitly `null` — and the connector doesn't cope with that. The sync errors out instead of just moving past those records, so I can't get a clean incremental sync to complete on streams where any record happens to have a null cursor value.

I'd expect the connector to tolerate this: if an individual record doesn't have a usable cursor value, the state advancement logic shouldn't crash the whole sync. Falling back to something sensible (e.g. the configured start date) for the purpose of state tracking would be fine — the important thing is the sync should keep running and finish, the way it does for records that do have a cursor value.

Reproducing is just "run an incremental sync against a Marketo account that has any record with a null `createdAt`/`updatedAt` in one of the incremental streams" — it consistently fails for me.
