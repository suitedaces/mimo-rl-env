## Problem Statement

I’m using awspec to check our AWS resources, but I can’t currently assert anything about CodeDeploy applications or their deployment groups. I’d like to be able to write specs that verify a CodeDeploy app and a deployment group exist, and also check that the deployment group is tied to the Auto Scaling group I expect.

## Expected outcomes

- CodeDeploy applications can be described with `codedeploy('...')`, support `exist`, and expose relevant application attributes such as `application_id`, `application_name`, `create_time`, `linked_to_git_hub`, `git_hub_account_name`, and `compute_platform`.
- CodeDeploy deployment groups can be described with `codedeploy_deployment_group('...')`, support `exist`, and expose relevant deployment group attributes such as `deployment_group_id`, `deployment_group_name`, `deployment_config_name`, `service_role_arn`, `compute_platform`, and `ecs_services`.
- `codedeploy_deployment_group('...')` can be scoped to a CodeDeploy application by passing `application_name: '...'` in the spec metadata; when no application name is supplied, it uses the default application name `default`.
- CodeDeploy deployment group specs support `have_autoscaling_group('...')` to verify that the deployment group is associated with the named Auto Scaling group.
- The resource type documentation includes entries and examples for `codedeploy` and `codedeploy_deployment_group`, including deployment group application scoping and Auto Scaling group matching.

## Implementation notes

- Follow awspec’s existing resource, matcher, and documentation conventions so the new CodeDeploy support behaves like other AWS resource types.
- The internal organization, helper structure, caching, and exact validation points are implementation details as long as the public awspec behavior above is satisfied.
