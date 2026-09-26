### MetalLB Version

v0.4.19

### Deployment method

Not relevant

### Main CNI

OVN-Kubernetes

### Kubernetes Version

v1.32.2

### Cluster Distribution

kind

### Describe the bug

No more details available than the title

### To Reproduce

No more details available than the title

### Expected Behavior

No dual stack IPs assigned for non dual stack clusters regardless of pool configuration

### Additional Context

Not available

### I've read and agree with the following

- [x] I've checked all open and closed issues and my request is not there.
- [x] I've checked all open and closed pull requests and my request is not there.

### I've read and agree with the following

- [x] I've checked all open and closed issues and my issue is not there.
- [x] This bug is reproducible when deploying MetalLB from the main branch
- [x] I have read the [troubleshooting guide](https://metallb.universe.tf/troubleshooting/) and I am still not able to make it work
- [x] I checked the logs and MetalLB is not discarding the configuration as not valid
- [x] I enabled the debug logs, collected the information required from the cluster using the [collect script](https://raw.githubusercontent.com/metallb/metallb/main/troubleshooting/collect.sh) and will attach them to the issue
- [x] I will provide the definition of my service and the related endpoint slices and attach them to this issue
