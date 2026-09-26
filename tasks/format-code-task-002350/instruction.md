## `get_checks_from_input_arn` returns far too many unrelated checks

I'm trying to use Prowler to audit specific resources by passing their ARNs (so we can run targeted scans against, say, one security group or one IAM user instead of an entire account). I noticed that the resulting check list is way bigger than I'd expect for a single ARN.

### What I'm doing

I'm calling `get_checks_from_input_arn` with a list containing a single ARN, e.g. an EC2 security group ARN like:

```
arn:aws:ec2:us-east-1:111122223333:security-group/sg-0123456789abcdef0
```

I expected to get back only the checks that actually apply to that resource type (security-group related EC2 checks). Instead I get a much larger set that includes EC2 checks for completely unrelated sub-services, and in some scenarios I've also seen checks from other services entirely.

I tried a few different ARNs to understand the pattern:

- An IAM user ARN (`arn:aws:iam::111122223333:user/some-user`) — I get back a bunch of IAM checks that have nothing to do with users (and some that look like password-policy checks bleeding in).
- An EC2 network ACL ARN — same kind of thing, the returned set includes checks for EBS, AMI, etc.
- ARNs for services that genuinely don't have a sub-service distinction (S3, KMS, GuardDuty, ELB, EFS) — these mostly look fine, I get the full set of checks for that service, which is what I want.

So the breakage seems specific to services where Prowler does have a sub-service notion: instead of narrowing down to the relevant sub-service, the filter behaves as if it's barely filtering at all.

### What I expect

When I pass an ARN, the returned set should be scoped to that resource:

- If Prowler can tell which sub-service the ARN refers to (e.g. `security-group`, `network-acl`, `user`, `snapshot`), the returned checks should be limited to that sub-service within the right service.
- If the ARN points at a service that doesn't really have sub-services in Prowler's model (S3, KMS, GuardDuty, ELB, EFS), it's reasonable to fall back to "all checks for that service".
- If for some reason no check in that service matches the parsed sub-service at all, falling back to the full service's checks is acceptable — but it should never spill across services, and it shouldn't return unrelated sub-services' checks alongside the matched ones.

Right now, for the sub-service-aware services, I'm getting something close to "all checks regardless of sub-service", which defeats the point of passing an ARN in the first place.

Could the filtering logic be tightened up so the scope actually matches the ARN? It would also be great to have test coverage for the various services / sub-services so this doesn't regress.
