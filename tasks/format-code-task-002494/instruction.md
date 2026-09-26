## Problem Statement

I’m configuring Addons for a project and it feels awkward that I have to set the main content selector separately for Doc diff and Link previews, even though they should both be looking at the same part of the page. Could there just be one project-level “main content” selector that any addon can use, and if I leave it blank it keeps doing the automatic detection?

## Expected outcomes

- Addons configuration exposes a single project-level `options_root_selector` value for the page’s main content CSS selector, shared by addons that need main-content detection.
- Leaving `options_root_selector` blank preserves automatic main-content detection instead of forcing a selector.
- The Addons configuration form shows `options_root_selector` with the label `CSS main content selector` and placeholder `[role=main]`.
- The previous per-addon root selector fields for Doc diff and Link previews are no longer editable configuration fields.
- Link previews documentation-tool metadata is no longer editable Addons configuration.
- Hosted-page addons configuration emits the shared selector at `addons.options.root_selector` and no longer emits per-addon selector or Link previews documentation-tool configuration.

## Implementation notes

- The exact model, form, migration, and serialization changes are up to the implementation, as long as the externally visible configuration, form, schema, and hosted-page payload behavior match the outcomes.
- Preserve existing Addons behavior outside the main-content selector consolidation.
