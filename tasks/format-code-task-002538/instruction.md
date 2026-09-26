## Persisting `job.meta` updates without overwriting the rest of the job

I'm using `job.meta` to track progress from inside a long-running task — something like:

```python
from rq import get_current_job

def process_big_thing(items):
    job = get_current_job()
    for i, item in enumerate(items):
        do_work(item)
        job.meta['progress'] = i / len(items)
        job.meta['last_item'] = item
        job.save()   # <-- persist progress so a dashboard can read it
```

The problem is that `job.save()` writes the *entire* job hash back to Redis (func, args, status, timestamps, everything from `to_dict()`). While my task is running, the worker and other parts of rq are also touching that same hash (status transitions, timestamps, etc.), so calling `save()` from inside the job to flush a `meta` update feels wrong — I'm effectively racing with whatever else is writing to that key, and any field I'm holding a stale copy of will get clobbered when my `save()` lands.

All I actually want is to push the updated `meta` dict back to Redis. I don't want to touch any of the other fields, and I don't want to have to `refresh()` first just to avoid trampling them.

Could there be a way to persist just the meta from a Job instance? Updating `job.meta` during execution and being able to flush it independently seems like a pretty common pattern (progress reporting, intermediate stats, etc.), and right now there's no clean way to do it.

The new method I'd expect on `Job` is something like `save_meta()`.
