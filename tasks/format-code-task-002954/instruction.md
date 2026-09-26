**What steps did you take and what happened:**
We have build a custom plugin for velero and we wanted to test the plugin. 

To consume the latest changes in the plugin we ran the following command :

`velero plugin add <registry/image:version>` 

the registry path had `_` in it and the command failed with

```
An error occurred: Deployment.apps "velero" is invalid: spec.template.spec.initContainers[1].name: Invalid value: "test_path-pluginX-2-pluginXX": a lowercase RFC 1123 label must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')
```


**What did you expect to happen:**
`_` should be allowed in the registry name, hence the `velero plugin add` command should not fail, when the registry path has `_` in it



**Anything else you would like to add:**
We did some investigation and found that this seems to be regression. The same command had worked for 1.5.4 release.

The regression is introduced between 1.5.4 to 1.6.0 RC2. 

This issue is seen in 1.6.0 GA version also

**Environment:**

- Velero version (use `velero version`):
  1.6.0
- Kubernetes version (use `kubectl version`):
  1.20
- Kubernetes installer & version:
   1.20
- Cloud provider or hardware configuration:

- OS (e.g. from `/etc/os-release`):
MAC


**Vote on this issue!**

This is an invitation to the Velero community to vote on issues, you can see the project's [top voted issues listed here](https://github.com/vmware-tanzu/velero/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc).  
Use the "reaction smiley face" up to the right of this comment to vote.

- :+1: for "I would like to see this bug fixed as soon as possible"
