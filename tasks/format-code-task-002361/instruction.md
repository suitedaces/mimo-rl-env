I created an AKS cluster, then went to import it.
```
pulumi import azure-native:containerservice:ManagedCluster cluster "/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourceGroups/workshop0e2eb622/providers/Microsoft.ContainerService/managedClusters/workshop-cluster4bdb372f"
```

It generated the following code:

```python
import pulumi
import pulumi_azure_native as azure_native

cluster = azure_native.containerservice.ManagedCluster("cluster",
    agent_pool_profiles=[azure_native.containerservice.ManagedClusterAgentPoolProfileArgs(
        count=1,
        enable_fips=False,
        kubelet_disk_type="OS",
        max_pods=50,
        mode="System",
        name="nodepool",
        orchestrator_version="1.21.9",
        os_disk_size_gb=30,
        os_disk_type="Ephemeral",
        os_sku="Ubuntu",
        os_type="Linux",
        type="VirtualMachineScaleSets",
        vm_size="Standard_DS3_v2",
        vnet_subnet_id="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourceGroups/workshop0e2eb622/providers/Microsoft.Network/virtualNetworks/workshop44dc0dd6/subnets/workshop",
    )],
    dns_prefix="workshop0e2eb622",
    enable_rbac=True,
    identity=azure_native.containerservice.ManagedClusterIdentityArgs(
        type="SystemAssigned",
    ),
    identity_profile={
        "kubeletidentity": azure_native.containerservice.ManagedClusterPropertiesIdentityProfileArgs(
            client_id="0d34de6d-772a-4087-a7e9-fbeb38fd3e12",
            object_id="2587d780-833c-4b99-baed-765c6add0dfc",
            resource_id="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourcegroups/MC_workshop0e2eb622_workshop-cluster4bdb372f_westus/providers/Microsoft.ManagedIdentity/userAssignedIdentities/workshop-cluster4bdb372f-agentpool",
        ),
    },
    kubernetes_version="1.21.9",
    location="westus",
    network_profile=azure_native.containerservice.ContainerServiceNetworkProfileArgs(
        dns_service_ip="10.0.0.10",
        docker_bridge_cidr="172.17.0.1/16",
        load_balancer_profile=azure_native.containerservice.ManagedClusterLoadBalancerProfileArgs(
            effective_outbound_ips=[azure_native.containerservice.ResourceReferenceArgs(
                id="/subscriptions/0282681f-7a9e-424b-80b2-96babd57a8a1/resourceGroups/MC_workshop0e2eb622_workshop-cluster4bdb372f_westus/providers/Microsoft.Network/publicIPAddresses/8fb08152-9185-4c60-beea-970a6c30f061",
            )],
            managed_outbound_ips=azure_native.containerservice.ManagedClusterLoadBalancerProfileManagedOutboundIPsArgs(
                count=1,
            ),
        ),
        load_balancer_sku="Standard",
        network_plugin="kubenet",
        outbound_type="loadBalancer",
        pod_cidr="10.244.0.0/16",
        service_cidr="10.0.0.0/16",
    ),
    node_resource_group="MC_workshop0e2eb622_workshop-cluster4bdb372f_westus",
    resource_group_name="workshop0e2eb622",
    resource_name="workshop0d45g994",
    service_principal_profile=azure_native.containerservice.ManagedClusterServicePrincipalProfileArgs(
        client_id="msi",
    ),
    sku=azure_native.containerservice.ManagedClusterSKUArgs(
        name="Basic",
        tier="Free",
    ),
    tags={
        "owner": "workshop",
        "purpose": "pulumi_workshop",
    },
    opts=pulumi.ResourceOptions(protect=True))
```

When I went to rerun the program, I got the following error:

```
Diagnostics:
  pulumi:pulumi:Stack (azure-refactor-cluster-dev):
    error: Program failed with an unhandled exception:
    error: Traceback (most recent call last):
      File "/Users/lbriggs/.asdf/installs/pulumi/3.28.0/bin/pulumi-language-python-exec", line 107, in <module>
        loop.run_until_complete(coro)
      File "/Users/lbriggs/.asdf/installs/python/3.9.2/lib/python3.9/asyncio/base_events.py", line 642, in run_until_complete
        return future.result()
      File "/Users/lbriggs/src/git/jaxxstorm/pulumi-refactoring-workshop/workspace/python/cluster/venv/lib/python3.9/site-packages/pulumi/runtime/stack.py", line 126, in run_in_stack
        await run_pulumi_func(lambda: Stack(func))
      File "/Users/lbriggs/src/git/jaxxstorm/pulumi-refactoring-workshop/workspace/python/cluster/venv/lib/python3.9/site-packages/pulumi/runtime/stack.py", line 49, in run_pulumi_func
        func()
      File "/Users/lbriggs/src/git/jaxxstorm/pulumi-refactoring-workshop/workspace/python/cluster/venv/lib/python3.9/site-packages/pulumi/runtime/stack.py", line 126, in <lambda>
        await run_pulumi_func(lambda: Stack(func))
      File "/Users/lbriggs/src/git/jaxxstorm/pulumi-refactoring-workshop/workspace/python/cluster/venv/lib/python3.9/site-packages/pulumi/runtime/stack.py", line 149, in __init__
        func()
      File "/Users/lbriggs/.asdf/installs/pulumi/3.28.0/bin/pulumi-language-python-exec", line 106, in <lambda>
        coro = pulumi.runtime.run_in_stack(lambda: runpy.run_path(args.PROGRAM, run_name='__main__'))
      File "/Users/lbriggs/.asdf/installs/python/3.9.2/lib/python3.9/runpy.py", line 285, in run_path
        return _run_code(code, mod_globals, init_globals,
      File "/Users/lbriggs/.asdf/installs/python/3.9.2/lib/python3.9/runpy.py", line 87, in _run_code
        exec(code, run_globals)
      File "./__main__.py", line 4, in <module>
        cluster = azure_native.containerservice.ManagedCluster("cluster",
    TypeError: __init__() got multiple values for argument 'resource_name'
    error: an unhandled error occurred: Program exited with non-zero exit code: 1
```

I removed the `resource_name` property and it looked fine. We probably need to omit the resource_name property?
