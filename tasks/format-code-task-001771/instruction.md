I've been hitting random AttributeErrors when some of my scripts/plugins try to treat the headline editor and the status line like normal text widgets — stuff like calling `disable()`/`enable()` on the body wrapper or the status line, or `setXScrollPosition`/`flashCharacter` on the headline wrapper just blows up because those methods don't exist on some of them but do on others. It'd be really nice if these wrapper classes all responded to the same basic API so I don't have to wrap every call in hasattr checks — even if they just no-op on widgets where it doesn't make sense, that'd be fine.

Expected outcomes:
- Generic code should be able to call the common text-widget compatibility operations on the affected body/text, status-line, and headline wrapper objects without first doing `hasattr` checks.
- Operations that do not make sense for a particular wrapper may safely be implemented as no-ops, but they should still be callable through the same public API shape used by comparable Leo wrappers.
- Query-style compatibility calls should return stable, simple values suitable for callers that only need to use the shared wrapper interface.

Implementation notes:
- Preserve existing behavior for widgets that already implement these operations.
- Use the existing wrapper/status-line conventions in the repository to determine the complete set of compatibility methods and call signatures that should be shared.
- The exact internal placement of the compatibility methods and any supporting organization are up to the implementer, as long as the public wrapper behavior is consistent.
