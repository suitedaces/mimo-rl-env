## Cross-thread recycling rate is noticeably lower than `io.netty.recycler.ratio` suggests

We use Netty's `Recycler` heavily for short-lived objects in a fairly typical
pattern: the object is acquired on one EventLoop thread and ends up being
released on a different thread (so it goes through the cross-thread / delayed
recycling path rather than being pushed directly onto the owning stack).

While tuning we added counters around `get()` / `recycle()` to see what
fraction of released objects actually make it back into the pool. With
default settings (`io.netty.recycler.ratio=8`) we expected the steady-state
retention rate to land somewhere around the configured 1/N regardless of
which thread does the recycling.

What we actually see:

- When the object is released on the same thread that allocated it, the
  observed retention rate matches the configured ratio quite well.
- When the object is released on a different thread, the retention rate is
  noticeably lower than the same-thread case, even though we're feeding
  both paths the same workload.

The gap is especially obvious in short-burst workloads: e.g. a worker that
only handles a handful of objects before going idle. In that regime the
same-thread path still manages to keep some of them, but the cross-thread
path effectively keeps none — every object that worker tried to return to
the pool was thrown away.

It looks like the cross-thread path applies the ratio differently from the
same-thread path; the configured ratio is supposed to be about the *rate*
of retention, not about systematically discarding the first chunk of items
that arrive from any given foreign thread. We'd like both paths to honor
the configured ratio consistently, so that whether an object is recycled
on its owning thread or shipped over from another thread doesn't materially
change how likely it is to survive.

Repro is just: allocate from a `Recycler` on thread A, hand the object to
thread B, call `recycle()` on B, and count how many pops on A actually
return a pooled instance vs. allocate a new one. Compare with the same
thing done entirely on thread A.
