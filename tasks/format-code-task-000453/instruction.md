Workflow can't be terminated because of the containerSet template that was referenced in the DAG task
## Summary

The problem occurs when running workflow with DAG task that is referencing `containerSet` template.

If you will try to terminate the workflow at the moment when DAG nodes have been initialized (in `Pending`) but not started yet, then the workflow will stuck at the running phase.

I pressed "Terminate" button when nodes `step-1` and `step-2` were created and the result displayed below:

![image](https://user-images.githubusercontent.com/58072595/151021410-28cfaa78-4f3e-4299-88eb-ee9614ff31ee.png)

## Diagnostics

The behavior is consistent and can be reproduced with the following workflow:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: container-set-termination-demo-
spec:
  entrypoint: main
  templates:
    - name: main
      dag:
        tasks:
          - name: using-container-set-template
            template: problematic-container-set
    - name: problematic-container-set
      containerSet:
        containers:
          - name: step-1
            image: alpine
            command:
            - sh
            - -c
            - "sleep 10"
          - name: step-2
            image: alpine
            command:
            - sh
            - -c
            - "sleep 10"
```
I have tried to change entrypoint from `main` to `problematic-container-set` and then the bug is not reproducible. So the issue is specific to DAG templates.

After the failed termination the workflow has following state:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  annotations:
    workflows.argoproj.io/pod-name-format: v1
  creationTimestamp: "2022-01-25T16:46:10Z"
  generateName: container-set-termination-demo-
  generation: 6
  labels:
    workflows.argoproj.io/phase: Running
    workflows.argoproj.io/resubmitted-from-workflow: container-set-termination-demo-rjx8r
  name: container-set-termination-demo-449lw
  namespace: argo
  resourceVersion: "45572"
  uid: cbbc9bb8-63c5-4ce1-abce-c8fe7192cdea
spec:
  activeDeadlineSeconds: 300
  arguments: {}
  entrypoint: main
  podSpecPatch: |
    terminationGracePeriodSeconds: 3
  shutdown: Terminate
  templates:
  - dag:
      tasks:
      - arguments: {}
        name: using-container-set-template
        template: problematic-container-set
    inputs: {}
    metadata: {}
    name: main
    outputs: {}
  - containerSet:
      containers:
      - command:
        - sh
        - -c
        - sleep 10
        image: alpine
        name: step-1
        resources: {}
      - command:
        - sh
        - -c
        - sleep 10
        image: alpine
        name: step-2
        resources: {}
    inputs: {}
    metadata: {}
    name: problematic-container-set
    outputs: {}
  ttlStrategy:
    secondsAfterCompletion: 600
status:
  artifactRepositoryRef:
    artifactRepository:
      archiveLogs: true
      s3:
        accessKeySecret:
          key: accesskey
          name: my-minio-cred
        bucket: my-bucket
        endpoint: minio:9000
        insecure: true
        secretKeySecret:
          key: secretkey
          name: my-minio-cred
    configMap: artifact-repositories
    key: default-v1
    namespace: argo
  conditions:
  - status: "False"
    type: PodRunning
  finishedAt: null
  nodes:
    container-set-termination-demo-449lw:
      children:
      - container-set-termination-demo-449lw-773192577
      displayName: container-set-termination-demo-449lw
      finishedAt: null
      id: container-set-termination-demo-449lw
      name: container-set-termination-demo-449lw
      phase: Running
      progress: 1/1
      startedAt: "2022-01-25T16:46:10Z"
      templateName: main
      templateScope: local/container-set-termination-demo-449lw
      type: DAG
    container-set-termination-demo-449lw-773192577:
      boundaryID: container-set-termination-demo-449lw
      children:
      - container-set-termination-demo-449lw-2800777053
      - container-set-termination-demo-449lw-2750444196
      displayName: using-container-set-template
      finishedAt: "2022-01-25T16:46:13Z"
      hostNodeName: k3d-argo-workflow-server-0
      id: container-set-termination-demo-449lw-773192577
      message: 'workflow shutdown with strategy:  Terminate'
      name: container-set-termination-demo-449lw.using-container-set-template
      phase: Failed
      progress: 1/1
      startedAt: "2022-01-25T16:46:10Z"
      templateName: problematic-container-set
      templateScope: local/container-set-termination-demo-449lw
      type: Pod
    container-set-termination-demo-449lw-2750444196:
      boundaryID: container-set-termination-demo-449lw-773192577
      displayName: step-2
      finishedAt: null
      id: container-set-termination-demo-449lw-2750444196
      name: container-set-termination-demo-449lw.using-container-set-template.step-2
      phase: Pending
      startedAt: "2022-01-25T16:46:10Z"
      templateName: problematic-container-set
      templateScope: local/container-set-termination-demo-449lw
      type: Container
    container-set-termination-demo-449lw-2800777053:
      boundaryID: container-set-termination-demo-449lw-773192577
      displayName: step-1
      finishedAt: null
      id: container-set-termination-demo-449lw-2800777053
      name: container-set-termination-demo-449lw.using-container-set-template.step-1
      phase: Pending
      startedAt: "2022-01-25T16:46:10Z"
      templateName: problematic-container-set
      templateScope: local/container-set-termination-demo-449lw
      type: Container
  phase: Running
  progress: 1/1
  startedAt: "2022-01-25T16:46:10Z"
```

---

> What version of Argo Workflows are you running?

v3.2.4

> What Kubernetes provider are you using?

k3d

> What executor are you running? Docker/K8SAPI/Kubelet/PNS/Emissary

Emissary

---

Not sure about the root cause right now, but I would like to try and dig in the code in order to find the problematic place. I will update once I will find something.

---
<!-- Issue Author: Don't delete this message to encourage other users to support your issue! -->
**Message from the maintainers**:

Impacted by this bug? Give it a 👍. We prioritise the issues with the most 👍.
