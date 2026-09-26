## Feature request: update a job's `data` after it has been added

Once a job is added to a queue with `Queue#add(data, opts)`, there doesn't seem to be any way to change its `data` payload afterwards. `Job#progress` lets me update progress, but `data` itself is effectively read-only from the public API.

I run into this in a couple of places:

- A job is added with some input, then before it gets picked up (or while it's being retried) I learn something new about it (e.g. a related record changed in the DB, a user edited the request) and I'd like the worker to see the updated payload instead of the stale one.
- I want to enrich the job's `data` with some computed fields during processing so that if the job is inspected later (via `getJob`, the UI, etc.) it carries the up-to-date information.

Right now my only options are either to remove and re-add the job (which loses its id and position) or to reach into Redis directly and overwrite the hash field, which feels like it shouldn't be necessary.

Could `Job` expose a method to update its `data`? Something I can call on a job instance to replace its stored data with a new object, and have subsequent reads (`Job.fromId`, the processor's `job.data` on the next fetch, etc.) reflect the new value.
