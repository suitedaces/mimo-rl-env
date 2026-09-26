## Problem Statement

我用 terrajet 把资源导出成 tfstate 之后，发现 refresh 阶段完全不理会我在 main.tf 里配的 operation timeouts，每次还是按默认超时走。我特地配了 read/create 这些超时，apply 的时候看着是生效的，但 refresh 还是该慢慢慢、该卡卡，感觉像是 refresh 根本没拿到我配的超时值。这是不是 tfstate 里少存了点什么？

## Expected outcomes

- `WriteTFState` should preserve configured non-zero operation timeout settings in the generated tfstate using a Terraform-compatible state representation observable by refresh.
- `WriteTFState` should omit timeout state metadata when no operation timeout is configured, and should not disturb any existing state metadata in that case.
- When existing state metadata is present, `WriteTFState` should preserve unrelated existing metadata while adding or updating the configured timeout information.
- `WriteMainTF` should keep its existing behavior for operation timeouts: configured non-zero timeout settings are emitted through the existing `timeouts` parameter in main.tf, and no `timeouts` parameter is emitted when all operation timeouts are unset.

## Implementation notes

The exact structure of helper code, data types, and validation placement is up to the implementer. The important requirement is that the generated tfstate and main.tf remain compatible with Terraform’s observable behavior for operation timeouts and preserve unrelated existing metadata.

## Required output literals (exact-match contract)

When `WriteTFState` emits configured operation timeouts into Terraform state private metadata, the decoded private metadata MUST contain Terraform's resource timeout metadata key exactly:

- State private metadata key: `e2bfb730-ecaa-11e6-8f88-34363bc7c4c0` — this is Terraform's resource timeout private-state compatibility key consumed by refresh.

Within that metadata object, configured operations MUST use Terraform's operation names exactly: `read`, `create`, `update`, and `delete`. Values MUST be Terraform-compatible duration nanosecond values.
