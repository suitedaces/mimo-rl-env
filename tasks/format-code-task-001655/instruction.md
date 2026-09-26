## Problem Statement

I want JSCS to catch lines where indentation mixes spaces and tabs, because right now our codebase can sneak in stuff like a space before a tab and the linter doesn't complain. It would be nice if there were a config option for this, ideally with a mode that still lets tabs plus spaces be used for alignment in places like docblocks.

## Expected outcomes

- JSCS accepts a `disallowMixedSpacesAndTabs` configuration option and runs the corresponding lint check when it is enabled.
- `disallowMixedSpacesAndTabs` accepts only `true` or `"smart"`; invalid values fail configuration with `disallowMixedSpacesAndTabs option requires true or "smart" value`.
- With `disallowMixedSpacesAndTabs: true`, a line containing adjacent spaces and tabs in either order reports `Mixed spaces and tabs found`; lines indented with only tabs or only spaces do not report this error.
- With `disallowMixedSpacesAndTabs: "smart"`, spaces followed by a tab report `Mixed spaces and tabs found`, while tabs followed by spaces are allowed for alignment.
- Docblock star alignment such as a tab followed by a single space before `*` or `*/` remains allowed when `disallowMixedSpacesAndTabs` is enabled.

## Implementation notes

The rule may be implemented using any structure that fits JSCS' existing configuration and checking flow. The exact parsing strategy, helper organization, and documentation wording are up to the implementer, as long as the externally observable configuration, validation, and lint results match the outcomes above.
