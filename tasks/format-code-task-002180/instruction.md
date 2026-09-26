## Default payload accepted on non-root workflow nodes

When configuring a multi-pipeline workflow, I noticed that a `payload` can be set on any node, not just the first one. This doesn't match how default payloads actually behave at runtime — they are only meaningful on the entry/root node of the workflow, since that's the one that gets triggered by hooks and where the payload is consumed.

### Repro via workflow-as-code

I have a yaml workflow like this:

```yaml
name: my-workflow
workflow:
  build:
    pipeline: build
  deploy:
    depends_on:
      - build
    pipeline: deploy
    payload:
      git.branch: master
      foo: bar
```

This imports without any error today, even though `deploy` is not the root of the workflow. The payload on `deploy` is silently kept but has no real effect, which is confusing — I only realized something was off when my hook didn't behave as I expected and I went looking at why.

I'd expect the import / save to refuse this configuration up front and tell me that a default payload cannot live on a non-root node.

### Same issue from the UI

I can also reach a broken state from the UI: if I take a node that already has a default payload defined and use the "add parent pipeline" action to put a new pipeline in front of it, the resulting workflow ends up with the default payload still attached to what is now a child node, while the new root has no payload at all. From the user's point of view the payload should follow the root, not stay on a node that no longer is one.

Symmetrically, when I add a child pipeline below an existing root, the dialog lets the new child carry its own default payload, which then gets persisted on a non-root node.

### Expected behavior

- Saving / importing a workflow where a non-root node carries a default payload should fail with a clear error, both for the API endpoint and for the yaml import path.
- The UI flows that add a parent or a child to an existing node should not produce a workflow where the default payload sits on anything other than the root node.
