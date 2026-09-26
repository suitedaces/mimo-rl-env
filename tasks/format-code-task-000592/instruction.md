## checkov misses resources in deeply nested Terraform child modules when scanning a tfplan JSON

I'm using checkov to scan the JSON output of `terraform show -json` against a Terraform project that has nested modules — my own module composes a couple of versioned upstream modules from the registry, so the resulting plan has child modules inside child modules.

When I scan the plan JSON, checkov picks up resources that are defined directly in the root module, and it also picks up resources from the immediate child modules. But the resources that live in the *next* level down — the ones declared inside a module that was itself instantiated by one of my child modules — never appear in the scan results at all. They aren't reported as passing, and they aren't reported as failing; checkov just behaves as if those resources don't exist.

Reproduction is roughly:

```hcl
# root main.tf
module "my_team_module" {
  source = "./modules/my_team_module"
  ...
}

# modules/my_team_module/main.tf
module "upstream" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "x.y.z"
  ...
}
```

```
terraform plan -out plan.out
terraform show -json plan.out > plan.json
checkov -f plan.json
```

The S3 bucket and related resources that the upstream module actually creates are visible in `plan.json` (under `planned_values.root_module.child_modules[...].child_modules[...].resources`), but they never show up in checkov's output. If I refactor the same code so that the upstream module is called directly from the root (i.e. only one level of nesting), those same resources are scanned correctly.

Composing modules out of other modules is a pretty normal pattern in Terraform, so this is a real blind spot when relying on checkov for plan-file scanning. Could `checkov -f plan.json` be made to find resources at any depth of module nesting, not just the first level?
