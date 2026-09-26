I'm hitting a bare `AssertionError` (no message at all) when conda tries to install into my env — the traceback just ends in `PrefixData.insert` with an empty assert, so I have no idea which package is the problem. It seems to happen after the solver finishes, during the actual write-out step. I dug a bit and it looks like the same package name shows up twice in what the solver decided to install, but I can't tell from the error which one it is. Could you take a look?

Expected outcomes:
- When conda computes the final set of package records for an environment operation, the result should not contain more than one record for the same package name.
- If insertion of a package record still encounters a duplicate package name, the raised `AssertionError` should include enough context to identify the conflicting package name and make the failure actionable instead of appearing as an empty assertion.

Implementation notes:
- The specific data structures, filtering location, and validation mechanism are up to the implementer.
- Preserve the existing solver and prefix write-out semantics except for eliminating duplicate-name records and improving the duplicate insertion failure message.
