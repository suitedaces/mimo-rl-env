Node kubectl unable to start due to incorrect Taints Argument
<!--
Thank you for opening this bug report! You are helping make eksctl a better project :)
In order to help us process this issue faster, please provide as much detail as possible.

When providing command examples, error output or code samples, please use code blocks.
For verbose output, for example logs, please either create a gist or use html details tags.
-->

<!--
Before you start writing, please search through existing issues to see whether your problem has already been reported.
For more information on how to open a bug report in eksctl, please refer to our issue submission guide.
https://github.com/weaveworks/eksctl/blob/main/CONTRIBUTING.md#opening-issues
-->

**What were you trying to accomplish?**
<!-- Information about the command you ran and what you expected to happen. -->

We tried to create a new nodegroup that was supposed to be added to the cluster.

The nodegroup had the config:

``` 
taints:
      controller: "true:NoSchedule"
```

**What happened?**
<!-- A description of actual behavior (with error messages). -->

The new nodegroup was created but failed to connect to the k8s cluster due to an invalid argument. An invalid `:` is at the beginning of the `--register-with-taints` argument.

**How to reproduce it?**
<!--
Include ALL the steps to reproduce the bug.

If using a config file, include it here, removing any sensitive information!
-->
Create a nodegroup with the following taints config using kubectl v0.47.0. (Tested on kubernetes 1.19)

``` 
taints:
      controller: "true:NoSchedule"
```

**Logs**
<!--
Include the output of the command line when running eksctl. If possible, eksctl should be run with debug logs. For example:
`eksctl get clusters -v 4`
Make sure you redact any sensitive information before posting.
If the output is long, please consider a Gist, or an html details tag.
-->

```
F0502 21:07:37.221415    8139 server.go:156] invalid argument "controllers=:true:NoSchedule" for "--register-with-taints" flag: invalid taint spec: controllers=:true:NoSchedule

``` 

**Anything else we need to know?**
<!--
What OS are you using?
Are you using a downloaded binary or did you compile eksctl?
What type of AWS credentials are you using (i.e. default/named profile, MFA)? - please don't include actual credentials though!
-->

The problem is only observed on v0.47.0. It works with eksctl v0.46.0.

This behavior is tested in: https://github.com/weaveworks/eksctl/blob/fc1f3b4b5ed6364777ad9d8160af9be241dd2319/pkg/nodebootstrap/ubuntu_test.go#L120

The case of `{"foo": "bar"}` is covered, but `{"foo": "true:bar"}` is not tested.


**Versions**
<!--
Please paste in the output of these commands:
-->
```
$ eksctl version
0.47.0

```
@Legion2
