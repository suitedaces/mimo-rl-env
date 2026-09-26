## Problem Statement

I'm seeing a couple of i18n formatting issues: when I forget to pass a value used by a UIString, `str_(...)` throws only `ICU Message contains a value reference ("wastedBytes") that wasn't provided`, and I can't tell which message it came from. I also noticed `{foo, number}` placeholders fed with `undefined` or a string end up formatting as `NaN`/garbage. In an older runtime using the Intl polyfills, plural ICU messages are failing with `Intl.PluralRules` missing.

## Expected outcomes

- Missing placeholder values: when formatting a localized UI string fails because a referenced placeholder value was not provided, the thrown error should identify both the missing reference and the ICU message that contained it.
- Numeric placeholders: placeholders declared for number formatting should reject non-`number` JavaScript values before producing formatted output, including `undefined` and strings.
- Numeric placeholder errors: failures for non-number numeric placeholder values should identify both the offending reference and the ICU message that contained it.
- Plural formatting compatibility: in runtimes that rely on the project’s Intl polyfill setup and do not provide native plural rules support, ICU plural messages should still be format-capable after i18n initialization.
- Existing formatting behavior: valid localized strings, including existing number formatting styles and plural messages with valid values, should continue to format successfully.

## Implementation notes

- The exact validation location, parser/formatter interaction, and data structures are implementation details.
- Preserve the existing public i18n formatting entry points and observable formatting behavior for valid inputs.
- Error text does not need to use a particular full sentence beyond clearly exposing the relevant ICU message and placeholder reference.
