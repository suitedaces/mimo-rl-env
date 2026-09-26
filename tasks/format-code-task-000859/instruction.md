Possibility to set preBootstrapCommands when using custom ami with managed nodegroups
<!--
Thank you for opening this feature request! You are helping make eksctl a better project :)
In order to help us process this request faster, please provide as much detail as possible.

Before creating a feature request, please search existing issues to see if this request has already been made. If there is a similar feature request please up-vote it and/or add your comments to it instead.

For more information on how to contribute to eksctl, please refer to our contributing docs.
https://github.com/weaveworks/eksctl/blob/main/CONTRIBUTING.md#opening-issues
-->

**What feature/behavior/change do you want?**
<!--
A clear and concise description of the change you would like to see in eksctl.

Do not hesitate, when appropriate, to share the exact commands or API you would like,
and/or to share a diagram (e.g.: asciiflow.com): "a picture is worth a thousand words".
-->
When pinning AMI for a managed nodegroup, currently eksctl ignores preBootstrapCommands. It would nice to have preBoostrapCommands.

AWS [blog](https://aws.amazon.com/blogs/containers/introducing-launch-template-and-custom-ami-support-in-amazon-eks-managed-node-groups/) talks about the workflow with eksctl, but eksctl does not respect preBootstrapCommands when using custom AMI.

![image](https://user-images.githubusercontent.com/1823272/127633255-bc580729-da78-4214-adb4-3c7c2399889e.png)

**Why do you want this feature?**
<!--
A clear and concise description of why you want this feature.
What is it you are trying to accomplish?
Include use-cases and any specific constraints you may have.
-->
This will allow us to do additional configuration before bootstrapping.
