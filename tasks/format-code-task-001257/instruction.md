## Problem Statement

I'm using moto's CloudFormation mocking, and my template has an `AWS::EC2::VPCGatewayAttachment` that attaches a VPN gateway via `VpnGatewayId`. When I call `create_stack`, it blows up with `KeyError: 'InternetGatewayId'`. On top of that, I'm also declaring an `AWS::EC2::VPNGateway` resource in the same template, and that doesn't seem to be recognized by moto's CloudFormation at all.

## Expected outcomes

- CloudFormation stack creation should support an `AWS::EC2::VPCGatewayAttachment` whose properties attach a VPN gateway by `VpnGatewayId`; creating such a stack should not fail because an internet gateway property is absent.
- The resulting mocked EC2 state should show the VPN gateway attached to the intended VPC after the stack is created.
- Existing CloudFormation support for `AWS::EC2::VPCGatewayAttachment` with `InternetGatewayId` should continue to create an internet gateway attachment successfully.
- CloudFormation should recognize and create `AWS::EC2::VPNGateway` resources with the standard required gateway type property and the optional Amazon-side ASN property.
- A CloudFormation-created `AWS::EC2::VPNGateway` should have a usable physical resource id so that other resources in the same template can reference it with `Ref`.

## Implementation notes

- Match moto’s existing CloudFormation resource modeling conventions and EC2 backend behavior.
- The exact internal structure, helper methods, and validation location are up to the implementer, as long as the externally observable CloudFormation and EC2 behavior above is satisfied.
