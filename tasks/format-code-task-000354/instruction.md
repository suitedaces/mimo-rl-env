### SecurityScan piling up multiple records per host

We push scan results into ralph from an external vulnerability scanner. The integration runs on a schedule and `POST`s the latest scan for each host to `/api/security-scans/` (using `host_ip` to identify the target).

After running this for a while I noticed that ralph keeps **every** scan we've ever submitted for a given host. So for a single machine I end up with dozens of `SecurityScan` rows, all pointing at the same `base_object`, and the API/admin happily lets them accumulate forever.

Conceptually that doesn't make sense for our use case — there is only ever one "current" scan result for a host. The previous one is stale the moment a new scan finishes; we don't want history, we want the latest state. The Security Info tab in the admin already kind of acknowledges this (it only shows one entry per host anyway), so the underlying data model storing N of them feels wrong.

What I'd expect:

- Re-`POST`ing a scan for a host that already has one should replace the previous one rather than add another row.
- Each host should only ever have one `SecurityScan` associated with it.

It would also be nice if existing databases (ours has been running for a while and already has the duplicates) got cleaned up to the "one per host" state when this is fixed — otherwise we'd have to write our own cleanup script before the new behaviour can be enforced.

Is there a reason scans were modelled as "many per host" originally? If not, can we move to a one-scan-per-host model?
