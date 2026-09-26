## Feature request: ability to delete a job's dependents when deleting the job

I'm using rq to run pipelines of jobs that depend on each other via `depends_on`. A typical setup looks like this:

```python
parent = queue.enqueue(do_step_one)
child  = queue.enqueue(do_step_two,  depends_on=parent)
grand  = queue.enqueue(do_step_three, depends_on=child)
```

If I decide partway through that I no longer want this pipeline to run and call `parent.delete()`, the parent job is removed but `child` and `grand` are left behind in Redis. They sit in the deferred registry forever pointing at a parent that no longer exists — they'll never be promoted to a queue (their dependency is gone) and they don't get cleaned up either. I end up having to walk the dependents set myself and call `delete()` on each one, recursively, which is awkward to do correctly from user code (especially when dependents themselves have dependents).

It would be really useful if `Job.delete()` could optionally take care of this cleanup itself — i.e. when I delete a job, give me a way to say "and also delete everything that was waiting on this job". The default behavior should stay as-is so existing code isn't affected.

Related discussion in #427 and #856.

I'd expect the API to look something like `job.delete(delete_dependents=True)`.
