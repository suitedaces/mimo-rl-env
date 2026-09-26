<!--
  Issues without logs and details are more complicated to fix.
  Please help us by filling the template below!
-->
### Related issue
 - #7644

### Expected behavior
 - deployed resources should be cleaned up with ``skaffold delete`` command

### Actual behavior
 - deployed resources are not released after running ``skaffold delete`` command


### Steps to reproduce the behavior

1. checkout main branch, and run make to build binary. 
2. run ``skaffold run`` in ``example/getting_started`` folder,
3. run ``skaffold delete`` to delete resources. 
4. run ``kubectl get pod``, should see ``getting_started`` pods are still running.  However, the expected behavior is all resources in the run should be cleaned up. 

### information 
 - Kubeclt deployer works for v1 as its clean up method is able to read the manifests configured for this deployer by calling Dependencies() method, so cleanUp method is able to release resource defined in those manifests. 
 - In v2, manifests are not defined under deployer, and schema upgrade will nil out kubectl deployer for old version schema as well. Cleanup method is not calling Dependencies(). However, even we call Dependencies() method, it returns nothing, so it won't fix the problem. 
 - As team discussed, we've decided to take advantages of manifests config in skaffold.yaml and use the rendered manifests as source data for resource deletion in v2. The implementation will #7644 as well
 - The engineering work may be easier after #7572 merged into main.

Note: I'd expect the `Runner.Render` entrypoint to be reused here, and `Cleanup` to take something like a `*manifest.ManifestListByConfig` so per-config rendered manifests can flow through.
