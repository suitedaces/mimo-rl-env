## Conditional modifiers for event format strings

Event format strings are used for dynamic index names, output keys, and other routing values, but today a field reference can only be mandatory or use the legacy `:fallback` form. Add shell-style conditional modifiers to field expansions so configurations can distinguish fallback, alternate, and required-value behavior without adding processors.

Support these forms on event-field references:

- `%{[field]:-fallback}` emits the field's converted string when it is available and non-empty; otherwise it emits `fallback`.
- `%{[field]:+alternate}` emits `alternate` when the converted field is available and non-empty; otherwise it emits an empty string. Values such as boolean `false` are available because their converted string is non-empty.
- `%{[field]:?message}` emits the converted field when it is available and non-empty; otherwise evaluation fails with an error containing the configured `message`.

For these modifiers, a value is unavailable when the field is missing, conversion to a string fails, or the converted string is empty. Different occurrences of the same field must apply their own modifiers independently. `Fields()` must continue returning unique field paths that can make evaluation fail: a field used by `:?` is required, while fields used only by `:-` or `:+` are not.

Apply the behavior consistently to `Run`, `RunBytes`, and `Eval`. On a required-value failure, `Run` returns an empty string, `RunBytes` returns a nil byte slice, and `Eval` must leave its caller-provided buffer unchanged, including any content already present before the call.

Each expansion accepts at most one modifier. Unknown modifiers, multiple modifiers on one expansion, and conditional modifiers on `%{+timestamp}` expansions must be rejected at compile time. Existing timestamp expansions without a modifier must continue to work. Preserve the existing `%{[field]:fallback}` behavior, including its fallback for missing, empty, or non-string-convertible values.
