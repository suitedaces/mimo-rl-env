# Problem Statement

Is there a way to assign IAM policy templates to target accounts using the IBM provider? I've got policy templates set up and I need to roll them out to specific accounts via Terraform, but I can't find a resource for it. Ideally I'd be able to specify which template version goes to which account and then reference back the assignment details (like the account ID, when it was created, and the status of what got created) in my outputs. It'd also be nice if I could point acceptance tests at a target account through an env var.

# Expected outcomes

- Terraform resource support:
  - Terraform configurations can declare an `ibm_iam_policy_assignment` managed resource without the provider rejecting the resource type as unsupported.
  - The resource lets users assign an IAM policy template/version to a target account using Terraform configuration.

- Resource input validation:
  - `version` is a required string input.
  - `target` is a required map input for the assignment target.
  - `templates` is required and accepts exactly one item; that item requires `id` and `version`.
  - `options` is required and accepts exactly one item; its nested `root` block is required and includes a required `requester_id`.
  - Missing required inputs, empty required blocks, or more than one `templates`/`options` item are rejected during Terraform validation or planning.
  - `accept_language` is optional and defaults to `default` when omitted.

- Resource state and outputs:
  - After a successful apply/read, `ibm_iam_policy_assignment` exposes assignment metadata that can be referenced in Terraform outputs, including `account_id`, `href`, `created_at`, `created_by_id`, `last_modified_at`, and `last_modified_by_id`.
  - The resource also exposes a computed `resources` list describing created assignment resources, including each item’s `target` and nested policy result information such as the created policy ID, status, and any error message details.

- Acceptance-test configuration:
  - Acceptance-test setup can read a target account from the `IBM_POLICY_ASSIGNMENT_TARGET_ACCOUNT_ID` environment variable.
  - When that environment variable is not set, the acceptance-test setup emits an informational message telling users to set it for `ibm_iam_policy_assignment` tests.

# Implementation notes

- Follow the provider’s existing conventions for Terraform managed resources, schema validation, state population, import/read/delete behavior, diagnostics, and acceptance-test configuration.
- The concrete internal structure, helper functions, mapping code, and validation placement are up to the implementation as long as the externally observable Terraform behavior above is satisfied.
- Tests should validate behavior through Terraform configuration/schema outcomes, resource state, diagnostics, and acceptance-test setup behavior rather than relying on private helper names or internal call paths.
