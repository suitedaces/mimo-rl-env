## Make `workflow.Cache` an interface

Currently `workflow.Cache` in `service/history/workflow` is a concrete struct, and everywhere in `service/history` that holds a reference to the cache holds it as `*workflow.Cache`. This makes the cache hard to substitute — for example, we can't easily plug in an alternative implementation, and unit tests that touch components depending on the cache (history engine, replicator, queue processors, task executors, workflow resetter, etc.) have no clean way to provide a fake.

It would be much more flexible if `workflow.Cache` were an interface that callers depend on, with the current struct becoming one concrete implementation behind it. Then anything in `service/history` that today holds `*workflow.Cache` would just hold the interface, and we'd be free to provide other implementations later without touching every call site.

No behavior change is expected for the existing implementation — this is purely about making the dependency abstract so it can be swapped.
