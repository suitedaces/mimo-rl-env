## Updating a plugin host catalog's attributes leaves the host sets under it with stale data

I have a plugin-backed host catalog with several host sets defined under it. The catalog's attributes are what the plugin uses to figure out which hosts to discover.

When I update those attributes (so that the plugin should be pulling a different population of hosts going forward), the host sets keep returning the same hosts they had cached from the previous sync. The contents of the sets don't reflect what the new attributes should produce.

If I just wait, eventually the periodic background sync catches up and the sets start showing the right hosts. But for some window after the update the sets are visibly out of date and there's no obvious way to nudge them.

This feels wrong to me — once the catalog's attributes change, the data the sets are currently holding was fetched under a different configuration, so it's not really guaranteed to be valid anymore. I'd expect that updating attributes on a catalog would cause the sets under that catalog to be refreshed (or at least not be left silently serving the old data until the next scheduled sync rolls around).
