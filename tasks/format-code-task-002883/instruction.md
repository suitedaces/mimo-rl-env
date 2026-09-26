# Problem Statement

I’m setting up Cloud Backup jobs and I need a way in the UI to choose whether restic stores absolute paths or relative paths. Could you add a “Use Absolute Paths” option on the Cloud Backup form, with a short tooltip, and make sure it isn’t changeable in cases where it wouldn’t make sense, like snapshot-based or existing jobs?

# Expected outcomes

- Cloud Backup creation exposes a “Use Absolute Paths” checkbox for configuring the submitted `absolute_paths` value.
- The “Use Absolute Paths” checkbox is unchecked by default when creating a new Cloud Backup job.
- When creating a Cloud Backup job, changing “Use Absolute Paths” changes the `absolute_paths` value submitted with the task.
- When “Take Snapshot” is enabled while creating a Cloud Backup job, “Use Absolute Paths” is forced off and cannot be edited.
- When “Take Snapshot” is disabled again while creating a Cloud Backup job, “Use Absolute Paths” becomes editable again.
- When editing an existing Cloud Backup job, “Use Absolute Paths” is visible but cannot be edited.
- The “Use Absolute Paths” field has tooltip/help text: “Determines whether restic backup will contain absolute or relative paths”.

# Implementation notes

- Preserve the existing Cloud Backup form behavior for unrelated fields and save flows.
- The placement, state-management approach, and validation location are up to the implementation as long as the user-visible form behavior and submitted `absolute_paths` value match the outcomes.
- Do not require users to configure anything outside the Cloud Backup form to use this option.
