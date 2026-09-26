### What problem does this address?

As part of the ongoing migration to the new 40px default size for form controls (see #65751), most components are being updated to opt into the larger default. `MenuItem` still appears to render at the old 36px height — you can see this in the `MenuItem` stories in Storybook, where the items look noticeably shorter than equivalent components that have already been migrated.

### Expected

`MenuItem` should render at the new 40px default height, consistent with other components that have been updated as part of the size migration effort.

### Actual

`MenuItem` still renders at 36px, so it's out of step with the rest of the design system migration.
