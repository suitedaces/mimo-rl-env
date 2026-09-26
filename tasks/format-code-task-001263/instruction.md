## Problem Statement

我在用 Moto mock boto3 的 SES/SESv2 测试邮件配置逻辑，现在卡在 configuration set 和 dedicated IP pool 这些接口上，像 create/get/list/delete 这类调用在 mock 里还跑不起来。能不能让 SESv2 至少能模拟 configuration set 和 dedicated IP pool 的基本生命周期，SES v1 也能把 configuration set 列出来、删掉？

## Expected Outcomes

- SESv2 configuration sets support a basic lifecycle through boto3: `sesv2.create_configuration_set(...)` creates a named configuration set, and `sesv2.get_configuration_set(ConfigurationSetName=...)` returns that name together with supported configuration option fields supplied at creation.
- SESv2 configuration sets can be listed with `sesv2.list_configuration_sets(...)`; the response contains the names of configuration sets currently present in the mock.
- SESv2 configuration sets can be deleted with `sesv2.delete_configuration_set(ConfigurationSetName=...)`; after deletion, the deleted configuration set is no longer returned by lookup or listing.
- SESv2 dedicated IP pools support a basic lifecycle through boto3: `sesv2.create_dedicated_ip_pool(PoolName=..., ScalingMode=...)` creates a pool, and `sesv2.get_dedicated_ip_pool(PoolName=...)` returns a `DedicatedIpPool` value containing the pool name and scaling mode.
- SESv2 dedicated IP pools can be listed and deleted with `sesv2.list_dedicated_ip_pools(...)` and `sesv2.delete_dedicated_ip_pool(PoolName=...)`; after deletion, the deleted pool is no longer returned by lookup or listing.
- SES v1 configuration sets can be listed with `ses.list_configuration_sets(...)`; the response contains created configuration set names and includes the `NextToken` response member expected by boto3 callers.
- SES v1 configuration sets can be deleted with `ses.delete_configuration_set(ConfigurationSetName=...)`; after deletion, the deleted configuration set no longer exists in SES v1 lookup or listing results.

## Implementation Notes

- Preserve Moto’s usual boto3-facing behavior for SES and SESv2 mocks; the internal storage model, validation location, and response rendering approach are up to the implementation.
- The lifecycle behavior should be observable through public boto3 SES/SESv2 client calls rather than through Moto internals.
- Keep behavior scoped to basic mock lifecycle support for the listed resources; do not require unrelated SES features to change.
