Manual trigger of SSH Keypair rotation - Infrastructure fails to be reconciled
**How to categorize this issue?**
/area control-plane
/kind bug
/priority 3

**What happened**:
When setting the `gardener.cloud/operation: rotate-ssh-keypair` annotation on the `shoot` after it was set already set previously the lastOperation shows the following error:
```
task "Waiting until shoot infrastructure has been reconciled" failed:
        Error while waiting for Infrastructure shoot--core--deleteme/deleteme to
        become ready: observed generation outdated (7/9)
```

When checking the `Infrastructure` resource  the `observedGeneration` and `generation` is out of sync and no reconcile is triggered after setting the `gardener.cloud/operation: rotate-ssh-keypair` annotation on the `shoot`. 

**What you expected to happen**:
That the `gardener.cloud/operation: rotate-ssh-keypair` annotation can be set on the `shoot` resource multiple times after it succeeded to rotate the SSH keypairs previsously.

**How to reproduce it (as minimally and precisely as possible)**:
1. Set `gardener.cloud/operation: rotate-ssh-keypair` annotation on a `shoot`
2. Wait until the reconciliation is done
3. You can verify on the `Infrastructure` resource that the `observedGeneration` and `generation` is out of sync 
4. Set `gardener.cloud/operation: rotate-ssh-keypair` annotation on the shoot again
5. After a few minutes the following error should be reported:
```yaml
status:
  lastErrors:
    - description: >-
        task "Waiting until shoot infrastructure has been reconciled" failed:
        Error while waiting for Infrastructure shoot--core--deleteme/deleteme to
        become ready: observed generation outdated (7/9)
      taskID: Waiting until shoot infrastructure has been reconciled
```

**Anything else we need to know?**:

**Environment**:

- Gardener version:
- Kubernetes version (use `kubectl version`):
- Cloud provider or hardware configuration:
- Others:
