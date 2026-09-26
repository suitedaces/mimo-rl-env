# Problem Statement

I'm running into an issue where if I pass a number into `setValue` or `addValue`, like `element.setValue(123)`, it blows up with a WebDriver error saying something like "Malformed type for 'text' parameter of command elementSendKeys / Expected: string / Actual: number". Same thing happens with `addValue(123)`. I expected I could just pass a number and have it typed into the field, but it seems like only strings work right now.

# Expected outcomes

- `element.addValue(value)` should accept numeric input and type its string representation instead of causing a WebDriver malformed-type error.
- `element.setValue(value)` should accept numeric input, clear the element as before, and then type the string representation instead of causing a WebDriver malformed-type error.
- The same non-string input handling should apply consistently across all supported execution paths.
- Existing string input behavior for `element.addValue(value)` and `element.setValue(value)` should remain unchanged.
- Other already-supported non-string inputs should be handled according to the project’s existing text-input conversion behavior, rather than being passed through as raw non-string protocol text parameters.

# Implementation notes

- The exact conversion mechanism, helper usage, and validation location are up to the implementation.
- Preserve the existing public command APIs and their observable behavior for string values.
- Avoid introducing protocol payloads that pass non-string values where text input commands require text.
