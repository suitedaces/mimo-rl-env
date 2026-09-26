## iam-role resource has no way to delete roles via a policy

I'm trying to write a Custodian policy that cleans up IAM roles that haven't been used in a long time. The `usage` filter on `iam-role` works well for finding them — e.g.:

```yaml
policies:
  - name: iam-delete-unused-role
    resource: iam-role
    filters:
      - type: usage
        match-operator: all
        LastAuthenticated: null
    actions:
      - delete
```

…but when I run this Custodian rejects the policy because `iam-role` doesn't actually have a `delete` action registered. Other IAM resources have actionable lifecycle support, so it's surprising that role deletion isn't there.

Could `iam-role` get a `delete` action so unused/stale roles can be cleaned up directly from a policy?

A couple of things I'd want the action to handle gracefully, since they come up routinely when sweeping a large account:

- Some roles will still be attached to an instance profile and AWS refuses to delete them in that state. The action shouldn't silently pretend it worked, but it also shouldn't be the kind of thing where one stuck role aborts the whole sweep before the other deletable roles are processed.
- When iterating over a batch, individual roles may have already been removed (e.g. by another process between list and delete) — that case should just be skipped rather than treated as a failure.
