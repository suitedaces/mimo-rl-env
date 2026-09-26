## Namespace deletions configured via the deletions manifest don't actually get deleted

We rely on CLM's `deletions` manifest to clean up resources that are no longer needed in our clusters. This works fine for most kinds, but Namespaces never actually get removed.

Our clusters enable a deletion-protection admission policy on Namespaces (see teapot/issues#1950 for the background) — to actually delete a protected Namespace, the caller has to first mark it with the agreed-upon "yes, I really want this gone" annotations on the Namespace's metadata. Only then will the API server let the delete through.

Today CLM's deletion path just calls delete on whatever Kind/Name is listed in the deletions config, without doing anything to satisfy that protection contract. So when we put something like:

```yaml
post_apply:
  - name: some-old-namespace
    kind: Namespace
```

into a deletions file, CLM logs that it's deleting it, but the Namespace stays around (or the delete is rejected by the admission webhook). For other Kinds that aren't protected, the same config works as expected.

It would be great if CLM handled this itself when processing deletions, so that listing a Namespace in the deletions config actually results in it being deleted, the same way it works for other resources. Cluster operators shouldn't have to manually pre-annotate every Namespace they want CLM to clean up.

This applies both when the deletion entry specifies a single `name:` and when it matches multiple resources via `labels:`.

For reference, the protection-bypass annotations our admission webhook expects are `zalando.org/delete-namespace` (set to the namespace's name) and `zalando.org/delete-date` (a timestamp).
