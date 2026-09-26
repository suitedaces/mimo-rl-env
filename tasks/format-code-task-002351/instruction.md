### Steps to Reproduce

Run a prowler aws scan that includes the `ec2_securitygroup_default_restrict_traffic` check against a new account with no resources configured:

```
prowler aws --checks ec2_securitygroup_default_restrict_traffic
```

### Expected behavior

The AWS check `ec2_securitygroup_default_restrict_traffic` should not produce `FAIL` findings, as there are no resources subject to a security group and no security groups have been created by the user.

### Actual Result with Screenshots or Logs

Prowler produces a `FAIL` result for _every default security group_ of _every default VPC_.

```sh
jq -r --arg CHECK_ID 'ec2_securitygroup_default_restrict_traffic' '.[] | select(.metadata.event_code == $CHECK_ID and .status_code == "FAIL") | .resources[0].region' < prowler-output-058264404402-20240523105507.ocsf.json
ap-northeast-1
ap-northeast-2
ap-northeast-3
ap-south-1
ap-southeast-1
ap-southeast-2
ca-central-1
eu-central-1
eu-north-1
eu-west-1
eu-west-2
eu-west-3
sa-east-1
us-east-1
us-east-2
us-west-1
us-west-2
```

The VPCs are completely unused and do not even have a public IP.

### How did you install Prowler?

Cloning the repository from github.com (git clone)

### Environment Resource

Workstation

### OS used

macOS

### Prowler version

4.1.0

### Pip version

24.0

### Context

AWS automatically creates a [default VPC in every region](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html). For every VPC, AWS [creates a default security group](https://docs.aws.amazon.com/vpc/latest/userguide/default-security-group.html).

The default security group has no ingress or egress rules associated with it -- it allows all traffic.

However,
a) the VPC is unused by default,
b) the VPC does not automatically have a public IP associated with it, even if it contains resources,
c) security groups are just one way to restrict access to resources in AWS, not the only one

**I don't think it's sensible to produce ~20 `High` `FAIL`s for an empty AWS account.**

Note: [a previous version of this check](https://github.com/prowler-cloud/prowler/pull/2777) instead checked if the security group "is open to the Internet". In some sense, this makes more sense to me. See https://github.com/prowler-cloud/prowler/issues/2761 for background on why this was changed.
