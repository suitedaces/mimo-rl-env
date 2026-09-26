public Api could create invalid workflow which has message Pod "" is invalid: spec.containers[1].image: Required value
Checklist:

 * [X] I've included the version.
 * [X] I've included reproduction steps.
 * [ ] I've included the workflow YAML.
 * [ ] I've included the logs.
 
**What happened**:

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
kubectl -n argo port-forward deployment/argo-server 2746:2746

POST http://localhost:2746/api/v1/workflows/argo-performance

POST Body: with wrong container properties imagex
```json
{
    "namespace": "argo-performance",
    "workflow": {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Workflow",
        "metadata": {
            "name": "hello-world-right-env-12"
        },
        "spec": {
            "entrypoint": "whalesay",
            "templates": [
                {
                    "name": "whalesay",
                    "container": {
                        "imagex": "docker/whalesay:latest",
                        "command": [
                            "cowsay"
                        ],
                        "args": [
                            "hello world"
                        ],
                        "env": []
                    }
                }
            ]
        }
    }
}
```

get response with status 200

```json
{
    "metadata": {
        "name": "hello-world-right-env-13",
        "namespace": "argo-performance",
        "selfLink": "/apis/argoproj.io/v1alpha1/namespaces/argo-performance/workflows/hello-world-right-env-13",
        "uid": "6466d400-0440-46e5-9a21-9f141ef17431",
        "resourceVersion": "2441046",
        "generation": 1,
        "creationTimestamp": "2020-06-11T13:21:28Z"
    },
    "spec": {
        "templates": [
            {
                "name": "whalesay",
                "arguments": {},
                "inputs": {},
                "outputs": {},
                "metadata": {},
                "container": {
                    "name": "",
                    "command": [
                        "cowsay"
                    ],
                    "args": [
                        "hello world"
                    ],
                    "resources": {}
                }
            }
        ],
        "entrypoint": "whalesay",
        "arguments": {}
    },
    "status": {
        "startedAt": null,
        "finishedAt": null
    }
}
```

get error from argo CLI

```bash
➜  ~ argo get hello-world-right-env-12 -n argo-performance
Name:                hello-world-right-env-12
Namespace:           argo-performance
ServiceAccount:      default
Status:              Error
Message:             Pod "hello-world-right-env-12" is invalid: spec.containers[1].image: Required value
Conditions:
 Completed           True
Created:             Thu Jun 11 21:08:49 +0800 (17 minutes ago)
Started:             Thu Jun 11 21:08:49 +0800 (17 minutes ago)
Finished:            Thu Jun 11 21:08:50 +0800 (17 minutes ago)
Duration:            1 second

STEP                         TEMPLATE  PODNAME                   DURATION  MESSAGE
 ⚠ hello-world-right-env-12  whalesay  hello-world-right-env-12  0s        Pod "hello-world-right-env-12" is invalid: spec.containers[1].image: Required value
```

**Anything else we need to know?**:

I cannot create this workflow via argo CLI
```bash
➜  argo git:(master) ✗ argo submit examples/hello-world.yaml -n argo-performance
2020/06/11 21:11:50 Failed to parse workflow: error unmarshaling JSON: while decoding JSON: json: unknown field "imagex"
```
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: hello-world-001
spec:
  entrypoint: whalesay
  templates:
  - name: whalesay
    container:
      imagex: docker/whalesay:latest
      command: [cowsay]
      args: ["hello world"]
      env: []
```

**Environment**:

- Argo version:
```
$ argo version
➜  ~ argo version
argo: v2.8.1
  BuildDate: 2020-05-28T23:40:32Z
  GitCommit: 0fff4b21c21c5ff5adbb5ff62c68e67edd95d6b8
  GitTreeState: clean
  GitTag: v2.8.1
  GoVersion: go1.13.4
  Compiler: gc
  Platform: darwin/amd64
```
- Kubernetes version :
```
$ kubectl version -o yaml
clientVersion:
  buildDate: "2020-04-16T23:35:15Z"
  compiler: gc
  gitCommit: 52c56ce7a8272c798dbc29846288d7cd9fbae032
  gitTreeState: clean
  gitVersion: v1.18.2
  goVersion: go1.14.2
  major: "1"
  minor: "18"
  platform: darwin/amd64
serverVersion:
  buildDate: "2020-01-15T08:18:29Z"
  compiler: gc
  gitCommit: e7f962ba86f4ce7033828210ca3556393c377bcc
  gitTreeState: clean
  gitVersion: v1.16.6-beta.0
  goVersion: go1.13.5
  major: "1"
  minor: 16+
  platform: linux/amd64
```

**Other debugging information (if applicable)**:

- workflow result:

```
argo --loglevel DEBUG get <workflowname>

DEBU[0000] CLI version                                   version="{v2.8.1 2020-05-28T23:40:32Z 0fff4b21c21c5ff5adbb5ff62c68e67edd95d6b8 v2.8.1 clean go1.13.4 gc darwin/amd64}"
DEBU[0000] Client options                                opts="{{ false false} 0x2175d40 0xc000111590}"
Name:                hello-world-right-env-12
Namespace:           argo-performance
ServiceAccount:      default
Status:              Error
Message:             Pod "hello-world-right-env-12" is invalid: spec.containers[1].image: Required value
Conditions:
 Completed           True
Created:             Thu Jun 11 21:08:49 +0800 (8 minutes ago)
Started:             Thu Jun 11 21:08:49 +0800 (8 minutes ago)
Finished:            Thu Jun 11 21:08:50 +0800 (8 minutes ago)
Duration:            1 second

STEP                         TEMPLATE  PODNAME                   DURATION  MESSAGE
 ⚠ hello-world-right-env-12  whalesay  hello-world-right-env-12  0s        Pod "hello-world-right-env-12" is invalid: spec.containers[1].image: Required value
```

- executor logs:

```
kubectl logs <failedpodname> -c init
kubectl logs <failedpodname> -c wait
```

- workflow-controller logs:

```
kubectl logs -n argo $(kubectl get pods -l app=workflow-controller -n argo -o name)
```

**Logs**

```
argo get <workflowname>
kubectl logs <failedpodname> -c init
kubectl logs <failedpodname> -c wait
kubectl logs -n argo $(kubectl get pods -l app=workflow-controller -n argo -o name)
```

---
<!-- Issue Author: Don't delete this message to encourage other users to support your issue! -->
**Message from the maintainers**:

If you are impacted by this bug please add a 👍 reaction to this issue! We often sort issues this way to know what to prioritize.
