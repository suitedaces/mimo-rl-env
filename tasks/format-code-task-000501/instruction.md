Tag AWS resources with the CLI version
[//]: #  (Before raising the feature request, please check to see if an existing feature request already exists.)


**Description**

[//]: #  (A short description of the feature you are proposing.)

AGC creates resources in AWS as part of `account activate` and `context deploy` commands. To aid in debugging and reporting, we should tag these resources with the version of AGC used to create them.

**Use Case**

[//]: #  (Why do you need this feature?)

When debugging, it may be important to know which version a resource was deployed under. For example, if a user upgrades and are using an older version of the resource, they may encounter issues.

When reporting on users, account managers may want to know which version of AGC their users are using.

**Proposed Solution**

[//]: #  (Please include prototype/workaround/sketch/reference implementation.)

Add a `agc-version` tag with the CLI version used to deploy that resource.
