Problem Statement: I noticed `jsdoc/valid-types` catches bad JSDoc types, but it seems to let completely empty inline tags like `{@link}` or `{@tutorial}` slip through, even inside a `@param` description. Could it report those as missing content instead of treating them as valid?

Expected outcomes:
- The `jsdoc/valid-types` rule should report `Inline tag "<tag>" missing content` when a link-style or tutorial inline tag has no content.
- This should hold both in the main JSDoc description and inside other tag descriptions such as `@param`.
- Inline tags with content should remain valid, and unrelated inline tags should not be treated as missing content.

Implementation notes:
- Only the externally visible lint result matters; traversal strategy, helper structure, and internal data organization are not part of the required contract.
