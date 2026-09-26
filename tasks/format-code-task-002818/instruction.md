## Problem Statement

我在用 terraform-provider-openstack 管理 DNS recordset，改了下 openstack_dns_recordset_v2 里的 ttl，比如从原来的值改成 3000，apply 完之后 terraform refresh 一拉发现服务端的 ttl 变成 0 了，跟我配的对不上，下次 plan 又有 diff。是我哪里写错了吗？

## Expected Outcomes

- Updating an existing `openstack_dns_recordset_v2` so that its configured `ttl` changes should persist the configured TTL in OpenStack DNS; a later refresh should read back the same TTL that is configured in Terraform.
- Updating other attributes of an `openstack_dns_recordset_v2` while leaving the configured `ttl` alone should not clear, reset, or otherwise alter the server-side TTL.
- Existing documented behavior for clearing a recordset-specific TTL or falling back to the service default should continue to work.
- Terraform state after apply and refresh should remain consistent with the configured recordset TTL, so a subsequent plan should not show a spurious TTL diff caused by the provider update request.

## Implementation Notes

- Preserve the existing public Terraform resource behavior and schema for `openstack_dns_recordset_v2`.
- The exact internal representation, helper structure, and validation location are up to the implementation, as long as the provider preserves the externally visible TTL behavior described above.
- Avoid changing unrelated DNS recordset behavior such as records, type, name, zone, or description handling except where necessary to keep update semantics consistent.
