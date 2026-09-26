Spot instances with Ephemeral OsDisk not working due to missing EvictionPolicy setting
/kind bug

**What steps did you take and what happened:**
```yaml
apiVersion: cluster.x-k8s.io/v1beta1
kind: MachinePool
metadata:
  name: st-005
  namespace: supplier-azure
  annotations:
    cluster.x-k8s.io/externally-managed-replicas: "true"
spec:
  clusterName: azure
  minReadySeconds: 0
  replicas: 1
  template:
    spec:
      bootstrap:
        configRef:
          apiVersion: bootstrap.cluster.x-k8s.io/v1beta1
          kind: KubeadmConfig
          name: st-005
      clusterName: azure-eu-v2
      infrastructureRef:
        apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
        kind: AzureMachinePool
        name: st-005
      version: v1.23.4
---
apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
kind: AzureMachinePool
metadata:
  name: st-005
  namespace: supplier-azure
spec:
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
    type: RollingUpdate
  location: westeurope
  template:
    image:
      sharedGallery:
        gallery: gallery
        name: linux-capi
        offer: OfferName
        resourceGroup: rg
        subscriptionID: ID
        sku: SKU
        version: 0.0.5
    osDisk:
      cachingType: ReadOnly
      diskSizeGB: 150
      osType: Linux
      diffDiskSettings:
        option: Local # ephemeral OS disk
    vmSize: Standard_F16s_v2
    spotVMOptions: {}
  identity: None
  additionalTags:
    cluster-autoscaler-enabled: "true"
    cluster-autoscaler-name: "azure"
    min: "0"
    max: "20"
---
apiVersion: bootstrap.cluster.x-k8s.io/v1beta1
kind: KubeadmConfig
metadata:
  name: st-005
  namespace: azure
spec:
  files:
    - contentFrom:
        secret:
          key: worker-node-azure.json
          name: st-005-azure-json
      owner: root:root
      path: /etc/kubernetes/azure.json
      permissions: "0644"
  format: cloud-config
  joinConfiguration:
    nodeRegistration:
      kubeletExtraArgs:
        azure-container-registry-config: /etc/kubernetes/azure.json
        cloud-config: /etc/kubernetes/azure.json
        cloud-provider: azure
      name: '{{ ds.meta_data["local_hostname"] }}'
```

Applying above resources result in an error:
```
capz-controller-manager-846765b8f4-fwskr manager E0819 12:46:28.180412       1 controller.go:317] controller/azuremachinepool "msg"="Reconciler error" "error"="failed to reconcile AzureMachinePool service scalesets: failed to start creating VMSS: cannot create VMSS: compute.VirtualMachineScaleSetsClient#CreateOrUpdate: Failure sending request: StatusCode=400 -- Original Error: Code=\"BadRequest\" Message=\"Azure Spot Virtual Machine Scale Sets with ephemeral OS disk support only 'Delete' evictionPolicy. For more information, see http://aka.ms/AzureSpot/errormessages.\"" "name"="st-005-2" "namespace"="supplier-azure" "reconciler group"="infrastructure.cluster.x-k8s.io" "reconciler kind"="AzureMachinePool"
```

EvictionPolicy is not configurable:
https://github.com/kubernetes-sigs/cluster-api-provider-azure/blob/main/azure/converters/spotinstances.go#L43

Always returns `Deallocate`. 

**What did you expect to happen:**
EvictionPolicy is configurable.

**Environment:**

-  cluster-api-provider-azure version: v1.4.1
- Kubernetes version: (use kubectl version): 1.23
- OS (e.g. from /etc/os-release): linux
