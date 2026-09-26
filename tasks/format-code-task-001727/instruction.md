Cannot create RRSet error while using external-dns controller with AWS network load balancer in the Jakarta (ap-southeast-3) region
<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

-->

**What happened**:

Hi there
While using this controller for a new EKS deployment in Jakarta I came across this error:

```
time="2022-05-11T16:24:15Z" level=info msg="Desired change: CREATE live.mydomain.com CNAME [Id: /hostedzone/Z0XXXXXXXXXXXXXXXX]"
time="2022-05-11T16:24:15Z" level=info msg="Desired change: CREATE live.mydomain.com TXT [Id: /hostedzone/Z0XXXXXXXXXXXXXXXX]"
time="2022-05-11T16:24:16Z" level=error msg="Failure in zone mydomain.com. [Id: /hostedzone/Z0XXXXXXXXXXXXXXXX]"
time="2022-05-11T16:24:16Z" level=error msg="InvalidChangeBatch: [RRSet of type TXT with DNS name live.mydomain.com. is not permitted because a conflicting RRSet of type CNAME with the same DNS name already exists in zone mydomain.com.]\n\tstatus code: 400, request id: 2154d259-edea-4a3b-b8ff-0c1cd9ac4fb6"
time="2022-05-11T16:24:16Z" level=error msg="failed to submit all changes for the following zones: [/hostedzone/Z0XXXXXXXXXXXXXXXX]"
```

I thought it was strange because I've run the controller with this setup in other regions without any issues at all.
Then after some research I came across this issue in Github:

https://github.com/kubernetes-sigs/external-dns/issues/1651

I think that to fix the problem there should be a new region added to the list for AWS Jakarta.
Also, it would be useful to have a warning message in the output if the region lookup fails. The error message is quite misleading and I spent a lot of time looking for phantom records.

**What you expected to happen**:

I expected new A ALIAS records to be created with the `live.mydomain.com` domain.

**How to reproduce it (as minimally and precisely as possible)**:

Use external-dns controller in the Jakarta `ap-southeast-3` region with Route53.

**Anything else we need to know?**:

**Environment**:
- External-DNS version (use `external-dns --version`): `0.11.1`
- DNS provider: AWS Route53
- Others: Region - Jakarta ap-southeast-3
