## cfn-lint passes invalid AWS::EC2::Subnet templates with IPAM pools

I've been migrating some of my CloudFormation VPC/Subnet code to use IPAM pools, and I noticed that cfn-lint is letting through Subnet templates that CloudFormation actually rejects at deploy time.

Two patterns I've hit:

**1. No CIDR source specified.** A Subnet needs either `CidrBlock` or `Ipv4IpamPoolId`. If neither is set (e.g. I refactored to switch from a hard-coded CIDR to IPAM and forgot to wire in the IPAM properties), cfn-lint reports no errors, but the stack fails to create:

```yaml
Resources:
  MySubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVpc
      AvailabilityZone: us-east-1a
      # no CidrBlock, no Ipv4IpamPoolId
```

**2. `Ipv4NetmaskLength` without `Ipv4IpamPoolId`.** I had a template where I'd set the netmask length but forgot to also set the IPAM pool id. cfn-lint accepts it, but the netmask length only makes sense paired with the pool id and the deploy fails:

```yaml
Resources:
  MySubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVpc
      Ipv4NetmaskLength: 24
      # missing Ipv4IpamPoolId
```

The second problem also shows up on `AWS::EC2::VPC` — cfn-lint will happily accept a VPC that sets `Ipv4NetmaskLength` on its own without `Ipv4IpamPoolId`.

Would be great if the schema for these resources caught these configurations at lint time so I get the errors before pushing to CloudFormation.
