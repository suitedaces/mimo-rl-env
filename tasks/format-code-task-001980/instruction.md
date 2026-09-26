## Top Crashers By Signature report doesn't expose GC crash count

I'm using the Top Crashers By Signature report to investigate which crash
signatures are most problematic, and I want to break the per-signature
numbers down by whether the crash happened during garbage collection.

Looking at the database schema, the underlying `tcbs` / `tcbs_build` tables
already track a per-row GC crash count (`is_gc_count`). But when I call
`getListOfTopCrashersBySignature` and look at what comes back for each
signature, I get the usual fields — `report_count`, `win_count`, `hang_count`,
`startup_count`, `plugin_count`, etc. — and no GC information at all. The
data is sitting in the table but the report just doesn't surface it, so
there's no way for me to tell, per top signature, how many of those crashes
were GC-related.

Could the Top Crashers By Signature report aggregate the GC crash counts
per signature and include them in the rows it returns, alongside the other
per-signature count fields?
