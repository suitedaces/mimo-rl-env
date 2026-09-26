The embedded SQLite dialect exposes CreateView and GetViewByName, and the engine already owns a persisted view catalog, but CreateView currently reports success without recording anything. This makes view registration look successful while later planning cannot discover the definition.

Make CreateView register a StackQL view definition in the SQLite catalog. A successful call must retain both the caller's raw view query and its translated SQL form, and GetViewByName must immediately find the active definition by the supplied name, returning that same name and raw query. A view body may be a SELECT or a UNION/UNION ALL of SELECTs.

Creating a view with an existing name is a replacement, not a duplicate. The replacement becomes the only active definition; preserve the prior catalog version as deleted so the catalog history retains one tombstone and one active row. The active lookup must expose the replacement's raw query, and the active catalog row must carry the replacement's translated SQL.

Reject a definition before changing the catalog when the name, raw query, or translated SQL is blank; when the raw query is syntactically invalid; or when it is not a SELECT/UNION query. Invalid calls must return an error and leave no active definition for that requested name.
