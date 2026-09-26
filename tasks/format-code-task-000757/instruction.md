## Updating `databricks_service_principal` on Azure fails

I'm managing service principals on an Azure Databricks workspace through Terraform. The service principal is backed by an existing Azure AD application (I pass the app GUID as `application_id`). Initial creation works fine, but any subsequent update to the resource fails on `terraform apply`.

Roughly what my config looks like:

```hcl
resource "databricks_service_principal" "sp" {
  application_id       = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # Azure AD app
  display_name         = "my-sp"
  allow_cluster_create = true
}
```

Repro:

1. `terraform apply` — succeeds, the service principal shows up in the workspace.
2. Change `display_name` (or flip one of the entitlement flags, e.g. `allow_cluster_create`).
3. `terraform apply` again — the update step errors out against the Databricks SCIM endpoint. The SP is left in a broken state for me.

If I then taint and recreate it, the create path works again — so it's specifically the update path.

I'm only seeing this on Azure workspaces; the same provider against an AWS workspace handles updates to service principals without complaints, so this looks Azure-specific.

Expected: once a service principal is created via this resource, I should be able to keep editing `display_name` / `active` / entitlements through normal `terraform apply` cycles without the update blowing up.
