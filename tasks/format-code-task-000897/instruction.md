`etcdctl lease keep-alive` has no way to renew just once and exit

Right now `etcdctl lease keep-alive <leaseID>` keeps the stream open and
keeps refreshing the lease until I kill it. That's fine for long-running
processes, but I'm calling etcdctl from a shell script where I just want
to bump a lease's TTL back to its full value at a specific point in time
and then let the script move on to the next step.

What I'd like to do roughly:

```
# ... do some work ...
etcdctl lease keep-alive <leaseID>   # I want this to renew once and return
# ... do more work ...
```

With the current behavior the command never returns, so I have to background
it and kill it, which is awkward and racy. The underlying clientv3 API
already supports a single-shot keep-alive, so it would be nice to expose
that through etcdctl as well — i.e. have a way to ask `lease keep-alive`
to reset the TTL one time and exit immediately.

A natural shape would be something like a `--once` flag on `lease keep-alive`.
