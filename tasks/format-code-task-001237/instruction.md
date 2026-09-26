Shoot conditions are not getting populated on first reconciliation
**How to categorize this issue?**
<!--
Please select area, kind, and priority for this issue. This helps the community categorizing it.
Replace below TODOs or exchange the existing identifiers with those that fit best in your opinion.
If multiple identifiers make sense you can also state the commands multiple times, e.g.
  /area control-plane
  /area auto-scaling
  ...

"/area" identifiers:     audit-logging|auto-scaling|backup|certification|control-plane-migration|control-plane|cost|delivery|dev-productivity|disaster-recovery|documentation|high-availability|logging|metering|monitoring|networking|open-source|ops-productivity|os|performance|quality|robustness|scalability|security|storage|testing|usability|user-management
"/kind" identifiers:     api-change|bug|cleanup|discussion|enhancement|epic|impediment|poc|post-mortem|question|regression|task|technical-debt|test
-->
/area control-plane
/kind bug

**What happened**:
When shoot is created its conditions such as `APISERVER`, `Control Plane` etc are not getting populated correctly in the shoot `status` on the first reconciliation of shoot. Though with the next reconciliation, these conditions are getting populated in shoot status correctly.

**What you expected to happen**:
When shoot is created it should set `APISERVER`, `Control Plane` etc other conditions properly in shoot status on the first reconciliation only.

**How to reproduce it (as minimally and precisely as possible)**:
Create a shoot with 629e94d066f09d0af2888e2511c19b6189b845e2 `Gardener` version and check the following:
```
$ kubectl get shoot -A -o wide                                                                                                                                                                                                                    

NAMESPACE      NAME    CLOUDPROFILE   PROVIDER   REGION   SEED    K8S VERSION   HIBERNATION   LAST OPERATION            STATUS    PURPOSE      GARDENER VERSION   APISERVER   CONTROL     NODES       SYSTEM     AGE
garden-local   local   local          local      local    local   1.25.4        Awake         Create Processing (10%)   healthy   evaluation   v1.63.0-dev        <unknown>   <unknown>   <unknown>   <unknown>    10m
```

Instead of condition to be `<unknown>` it should have been set to `Progressing` or `Unknown` as per shoot healthiness as follows:

```
NAMESPACE      NAME    CLOUDPROFILE   PROVIDER   REGION   SEED    K8S VERSION   HIBERNATION   LAST OPERATION            STATUS    PURPOSE      GARDENER VERSION   APISERVER   CONTROL       NODES         SYSTEM        AGE
garden-local   local   local          local      local    local   1.25.4        Awake         Create Processing (81%)   healthy   evaluation   v1.63.0-dev        True        Progressing   Progressing   Progressing   3m5s
```

**Anything else we need to know?**:
It happens if shoot has no seed name in spec during creation.
It works with commit 73059233c0214553fa3ce79b21cbc777ff563ac7. So probably this issue is introduced with #7206.

**Environment**: provider-local

- Gardener version: 629e94d066f09d0af2888e2511c19b6189b845e2
- Kubernetes version (use `kubectl version`):
- Cloud provider or hardware configuration:
- Others:
