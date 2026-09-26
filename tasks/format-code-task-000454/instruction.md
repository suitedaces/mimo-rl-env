Internal Server Error When Fetching Logs From Inline Workflows
### Pre-requisites

- [X] I have double-checked my configuration
- [X] I can confirm the issues exists when I tested with `:latest`
- [ ] I'd like to contribute the fix myself (see [contributing guide](https://github.com/argoproj/argo-workflows/blob/master/docs/CONTRIBUTING.md))

### What happened/what you expected to happen?

### What happened?
When I run a workflow that contains an inline component, I cannot view the logs for that container. The Argo UI shows an "Internal Server Error". However, when I check the minio browser, I can find the main.log file and retrieve it's contents without any issues.

This issue only occurs on inline components. When running other types of templates, I don't see this issue. 

For example, these workflows run fine and I can see the logs in the Argo UI:
[hello-world](https://github.com/argoproj/argo-workflows/blob/master/examples/hello-world.yaml)
[steps](https://github.com/argoproj/argo-workflows/blob/master/examples/steps.yaml)

But, these workflows recreate the issue:
[steps-inline-workflow](https://github.com/argoproj/argo-workflows/blob/master/examples/steps-inline-workflow.yaml)
[dag-inline-workflow](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-inline-workflow.yaml)

This issue also occurs with actual artifacts coming from containers. For example I can run a simple argosay container and generate a .txt file that shows up in the Argo UI. However if I move that container into an inline definition, the logs, and the artifact itself throw errors in the UI (while showing up just fine in minio). 

### What you expected to happen?
I expected the logs and the artifacts to be accessible from the Argo UI despite the container being defined as inline.


### Version

3.4.1 and latest

### Paste a small workflow that reproduces the issue. We must be able to run the workflow; don't enter a workflows that uses private images.

```YAML
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: hello-world-
  labels:
    workflows.argoproj.io/archive-strategy: "false"
spec:
  entrypoint: main
  templates:
  - name: main
    steps:
      - - name: a
          inline:
            container:
              image: argoproj/argosay:v2
              args: [ echo, hello, /mnt/file.txt ]
            outputs:
              artifacts:
                - name: file
                  path: /mnt/file.txt
                  archive:
                    none: { }
```


### Logs from the workflow controller

```
time="2022-10-14T18:50:19.077Z" level=info msg="Update leases 200"
time="2022-10-14T18:50:24.082Z" level=info msg="Get leases 200"
time="2022-10-14T18:50:24.087Z" level=info msg="Update leases 200"
time="2022-10-14T18:50:29.093Z" level=info msg="Get leases 200"
time="2022-10-14T18:50:29.097Z" level=info msg="Update leases 200"
time="2022-10-14T18:50:34.101Z" level=info msg="Get leases 200"
time="2022-10-14T18:50:34.106Z" level=info msg="Update leases 200"
time="2022-10-14T18:50:36.217Z" level=info msg="Processing workflow" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.221Z" level=info msg="Get configmaps 200"
time="2022-10-14T18:50:36.221Z" level=info msg="resolved artifact repository" artifactRepositoryRef="quilter-dev-sergiy/#"
time="2022-10-14T18:50:36.221Z" level=info msg="Updated phase  -> Running" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.221Z" level=info msg="Steps node hello-world-62qpl initialized Running" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.221Z" level=info msg="StepGroup node hello-world-62qpl-2899326954 initialized Running" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.222Z" level=info msg="Pod node hello-world-62qpl-75685911 initialized Pending" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.226Z" level=info msg="Create events 201"
time="2022-10-14T18:50:36.246Z" level=info msg="Create pods 201"
time="2022-10-14T18:50:36.247Z" level=info msg="Created pod: hello-world-62qpl[0].a (hello-world-62qpl--75685911)" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.248Z" level=info msg="Workflow step group node hello-world-62qpl-2899326954 not yet completed" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.248Z" level=info msg="TaskSet Reconciliation" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.248Z" level=info msg=reconcileAgentPod namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:36.248Z" level=info msg="Workflow to be dehydrated" Workflow Size=1661
time="2022-10-14T18:50:36.255Z" level=info msg="Update workflows 200"
time="2022-10-14T18:50:36.255Z" level=info msg="Workflow update successful" namespace=quilter-dev-sergiy phase=Running resourceVersion=494580351 workflow=hello-world-62qpl
time="2022-10-14T18:50:36.263Z" level=info msg="Create events 201"
time="2022-10-14T18:50:36.268Z" level=info msg="Create events 201"
time="2022-10-14T18:50:39.111Z" level=info msg="Get leases 200"
time="2022-10-14T18:50:39.115Z" level=info msg="Update leases 200"
time="2022-10-14T18:50:44.119Z" level=info msg="Get leases 200"
time="2022-10-14T18:50:44.123Z" level=info msg="Update leases 200"
time="2022-10-14T18:50:46.248Z" level=info msg="Processing workflow" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="Task-result reconciliation" namespace=quilter-dev-sergiy numObjs=0 workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=warning msg="workflow uses legacy/insecure pod patch, see https://argoproj.github.io/argo-workflows/workflow-rbac/" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="node changed" namespace=quilter-dev-sergiy new.message= new.phase=Succeeded new.progress=0/1 nodeID=hello-world-62qpl-75685911 old.message= old.phase=Pending old.progress=0/1 workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="Step group node hello-world-62qpl-2899326954 successful" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="node hello-world-62qpl-2899326954 phase Running -> Succeeded" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="node hello-world-62qpl-2899326954 finished: 2022-10-14 18:50:46.249907957 +0000 UTC" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="Outbound nodes of hello-world-62qpl-75685911 is [hello-world-62qpl-75685911]" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="Outbound nodes of hello-world-62qpl is [hello-world-62qpl-75685911]" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.249Z" level=info msg="node hello-world-62qpl phase Running -> Succeeded" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="node hello-world-62qpl finished: 2022-10-14 18:50:46.249998697 +0000 UTC" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="Checking daemoned children of hello-world-62qpl" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="TaskSet Reconciliation" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg=reconcileAgentPod namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="Updated phase Running -> Succeeded" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="Marking workflow completed" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="Marking workflow as pending archiving" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="Checking daemoned children of " namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.250Z" level=info msg="Workflow to be dehydrated" Workflow Size=2376
time="2022-10-14T18:50:46.256Z" level=info msg="Create events 201"
time="2022-10-14T18:50:46.256Z" level=info msg="cleaning up pod" action=deletePod key=quilter-dev-sergiy/hello-world-62qpl-1340600742-agent/deletePod
time="2022-10-14T18:50:46.259Z" level=info msg="Update workflows 200"
time="2022-10-14T18:50:46.260Z" level=info msg="Workflow update successful" namespace=quilter-dev-sergiy phase=Succeeded resourceVersion=494580468 workflow=hello-world-62qpl
time="2022-10-14T18:50:46.261Z" level=info msg="Delete pods 404"
time="2022-10-14T18:50:46.263Z" level=info msg="DeleteCollection workflowtaskresults 403"
time="2022-10-14T18:50:46.263Z" level=warning msg="failed to delete task-results" error="workflowtaskresults.argoproj.io is forbidden: User \"system:serviceaccount:quilter-dev-sergiy:argo\" cannot deletecollection resource \"workflowtaskresults\" in API group \"argoproj.io\" in the namespace \"quilter-dev-sergiy\"" namespace=quilter-dev-sergiy workflow=hello-world-62qpl
time="2022-10-14T18:50:46.264Z" level=info msg="archiving workflow" namespace=quilter-dev-sergiy uid=bf991edf-8f3c-476e-9e53-9eb88785748d workflow=hello-world-62qpl
time="2022-10-14T18:50:46.265Z" level=info msg="Create events 201"
time="2022-10-14T18:50:46.268Z" level=info msg="Create events 201"
time="2022-10-14T18:50:46.268Z" level=info msg="cleaning up pod" action=labelPodCompleted key=quilter-dev-sergiy/hello-world-62qpl--75685911/labelPodCompleted
time="2022-10-14T18:50:46.273Z" level=info msg="Create events 201"
```

### Logs from in your workflow's wait container

```
time="2022-10-14T18:50:40.662Z" level=info msg="S3 Save path: /tmp/argo/outputs/logs/main.log, key: hello-world-62qpl/hello-world-62qpl--75685911/main.log"
time="2022-10-14T18:50:40.662Z" level=info msg="Creating minio client using static credentials" endpoint="minio:9000"
time="2022-10-14T18:50:40.663Z" level=info msg="Saving file to s3" bucket=my-bucket endpoint="minio:9000" key=hello-world-62qpl/hello-world-62qpl--75685911/main.log path=/tmp/argo/outputs/logs/main.log
time="2022-10-14T18:50:40.671Z" level=info msg="Save artifact" artifactName=main-logs duration=8.212867ms error="<nil>" key=hello-world-62qpl/hello-world-62qpl--75685911/main.log
time="2022-10-14T18:50:40.671Z" level=info msg="not deleting local artifact" localArtPath=/tmp/argo/outputs/logs/main.log
time="2022-10-14T18:50:40.671Z" level=info msg="Successfully saved file: /tmp/argo/outputs/logs/main.log"
time="2022-10-14T18:50:40.677Z" level=info msg="Create workflowtaskresults 403"
time="2022-10-14T18:50:40.678Z" level=warning msg="failed to patch task set, falling back to legacy/insecure pod patch, see https://argoproj.github.io/argo-workflows/workflow-rbac/" error="workflowtaskresults.argoproj.io is forbidden: User \"system:serviceaccount:quilter-dev-sergiy:default\" cannot create resource \"workflowtaskresults\" in API group \"argoproj.io\" in the namespace \"quilter-dev-sergiy\""
time="2022-10-14T18:50:40.695Z" level=info msg="Patch pods 200"
time="2022-10-14T18:50:40.700Z" level=info msg="Alloc=11442 TotalAlloc=17630 Sys=22738 NumGC=5 Goroutines=12"
```
