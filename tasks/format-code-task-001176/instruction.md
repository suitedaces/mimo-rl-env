Taurus supports reusable JMeter request fragments through `include-scenario`, but the configuration linter currently validates only execution-level scenario references. Bad include targets and recursive compositions therefore survive linting and fail later while a test plan is being built. Extend the public `ConfigurationLinter` behavior so lint-only CI catches these problems before execution. Because linting itself does not process XML, importing and using the linter must also work in a minimal installation where the optional `lxml` package cannot be imported.

Inspect every named scenario, whether or not an execution currently references it, and every scenario dictionary embedded directly in an execution. Start at each scenario's `requests` list. Descend into `then` and `else` request lists for `if` blocks, the request list stored directly in a `once` block, and the `do` request lists of `loop`, `while`, `foreach`, and `transaction` blocks. A matching key inside an arbitrary request payload such as `body` is data, not an include block, and must not be linted as one.

For each real include block:

- `include-scenario` must be a non-empty string. Every violating occurrence produces one `ConfigWarning.ERROR` with identifier `invalid-include-scenario`.
- A string target is defined when that exact key is present in top-level `scenarios`; do not use the target value's truthiness to decide existence. Every missing occurrence produces one `ConfigWarning.ERROR` with identifier `undefined-include-scenario`, and its message identifies the missing alias.
- Every new warning path is the full dotted path from the configuration root through the offending `include-scenario` value.

Treat includes between named scenarios as a directed graph. A direct self-include and every edge in a multi-scenario cycle produce `ConfigWarning.ERROR` with identifier `recursive-include-scenario`. Report exactly once for each source include occurrence whose edge participates in a cycle: repeated include blocks retain their distinct paths, while referencing or executing the same scenario multiple times must not duplicate its findings. Shared sub-scenarios and repeated edges in an acyclic graph are valid and produce no include diagnostic.

The three new warning identifiers must honor the existing `ignored-warnings` filter. Calling `lint()` again on the same linter replaces the previous findings instead of accumulating duplicates. Preserve the existing `possible-typo` diagnostic for misspelled execution fields and `undefined-scenario` diagnostic for missing execution-level scenario aliases.
