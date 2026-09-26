validate_cluster ignoring node with role "spot-worker"
Thanks for submitting an issue! Please fill in as much of the template below as
you can.

------------- BUG REPORT TEMPLATE --------------------

1. What `kops` version are you running? The command `kops version`, will display
 this information.

Version 1.9.0 (git-cccd71e67)

2. What Kubernetes version are you running? `kubectl version` will print the
 version if a cluster is running or provide the Kubernetes version specified as
 a `kops` flag.

```
Client Version: version.Info{Major:"1", Minor:"9", GitVersion:"v1.9.2", GitCommit:"5fa2db2bd46ac79e5e00a4e6ed24191080aa463b", GitTreeState:"clean", BuildDate:"2018-01-18T10:09:24Z", GoVersion:"go1.9.2", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"8", GitVersion:"v1.8.11", GitCommit:"1df6a8381669a6c753f79cb31ca2e3d57ee7c8a3", GitTreeState:"clean", BuildDate:"2018-04-05T17:16:46Z", GoVersion:"go1.8.3", Compiler:"gc", Platform:"linux/amd64"}
```

3. What cloud provider are you using?

AWS

4. What commands did you run?  What is the simplest way to reproduce this issue?

`kops validate cluster`

5. What happened after the commands executed?

It printed an unexpected warning:

```
$ kops validate cluster staging
Validating cluster staging

W0418 20:13:21.035353    3316 validate_cluster.go:275] ignoring node with role "spot-worker"
W0418 20:13:21.035379    3316 validate_cluster.go:275] ignoring node with role "spot-worker"
W0418 20:13:21.035398    3316 validate_cluster.go:275] ignoring node with role "spot-worker"
INSTANCE GROUPS
NAME                    ROLE    MACHINETYPE     MIN     MAX     SUBNETS
master-us-east-1c       Master  m3.medium       1       1       us-east-1c
nodes                   Node    c4.xlarge       1       5       us-east-1c

NODE STATUS
NAME                            ROLE    READY
ip-172-20-39-155.ec2.internal   master  True

Your cluster staging is ready
```

6. What did you expect to happen?

It wouldn't have any issue with the node role.

7. Please provide your cluster manifest. 
```
$ kops get -o yaml --name staging
apiVersion: kops/v1alpha2
kind: Cluster
metadata:
  creationTimestamp: 2018-01-23T23:26:25Z
  name: staging
spec:
  additionalPolicies:
    node: |
      [{
        "Sid": "Stmt1519813867626",
        "Action": ["ec2:DescribeSpotPriceHistory"],
        "Effect": "Allow",
        "Resource": "*"
      }]
  api:
    dns: {}
  authorization:
    rbac: {}
  channel: stable
  cloudProvider: aws
  configBase: s3://clusters/staging
  etcdClusters:
  - etcdMembers:
    - instanceGroup: master-us-east-1c
      name: c
    name: main
  - etcdMembers:
    - instanceGroup: master-us-east-1c
      name: c
    name: events
  iam:
    allowContainerRegistry: true
    legacy: false
  kubeAPIServer:
    admissionControl:
    - Initializers
    - NamespaceLifecycle
    - LimitRanger
    - ServiceAccount
    - PersistentVolumeLabel
    - DefaultStorageClass
    - DefaultTolerationSeconds
    - NodeRestriction
    - Priority
    - PersistentVolumeClaimResize
    - ResourceQuota
    authorizationRbacSuperUser: admin
    featureGates:
      ExpandPersistentVolumes: "true"
  kubeControllerManager:
    featureGates:
      ExpandPersistentVolumes: "true"
    horizontalPodAutoscalerDownscaleDelay: 30m0s
    horizontalPodAutoscalerSyncPeriod: 1m0s
    horizontalPodAutoscalerUpscaleDelay: 5m0s
    horizontalPodAutoscalerUseRestClients: true
  kubelet:
    enableCustomMetrics: true
    featureGates:
      ExpandPersistentVolumes: "true"
  kubernetesApiAccess:
  - 0.0.0.0/0
  kubernetesVersion: 1.8.11
  masterInternalName: api.internal.staging
  masterPublicName: api.staging
  networkCIDR: 172.20.0.0/16
  networking:
    kubenet: {}
  nonMasqueradeCIDR: 100.64.0.0/10
  sshAccess:
  - 0.0.0.0/0
  subnets:
  - cidr: 172.20.32.0/19
    name: us-east-1c
    type: Public
    zone: us-east-1c
  topology:
    dns:
      type: Public
    masters: public
    nodes: public

---

apiVersion: kops/v1alpha2
kind: InstanceGroup
metadata:
  creationTimestamp: 2018-01-23T23:26:31Z
  labels:
    kops.k8s.io/cluster: staging
  name: master-us-east-1c
spec:
  image: kope.io/k8s-1.8-debian-jessie-amd64-hvm-ebs-2018-01-14
  machineType: m3.medium
  maxSize: 1
  minSize: 1
  nodeLabels:
    kops.k8s.io/instancegroup: master-us-east-1c
  role: Master
  subnets:
  - us-east-1c

---

apiVersion: kops/v1alpha2
kind: InstanceGroup
metadata:
  creationTimestamp: 2018-01-23T23:26:31Z
  labels:
    kops.k8s.io/cluster: staging
  name: nodes
spec:
  cloudLabels:
    k8s.io/cluster-autoscaler/enabled: "yes"
    kubernetes.io/cluster/staging: "true"
  image: kope.io/k8s-1.8-debian-jessie-amd64-hvm-ebs-2018-01-14
  machineType: c4.xlarge
  maxPrice: "0.4"
  maxSize: 5
  minSize: 1
  nodeLabels:
    kops.k8s.io/instancegroup: nodes
    node-role.kubernetes.io/spot-worker: "true"
  role: Node
  rootVolumeSize: 64
  rootVolumeType: gp2
  subnets:
  - us-east-1c
```

9. Anything else do we need to know?

It seems like there is some logic to determine the node "role" by looking at any labels on the node that start with `node-role.kubernetes.io/`.  However, it seems that a node could have multiple roles.

The code to check whether a node or "master" or "node" should work with lists / sets of roles instead of using the last role found in the labels as the role.
