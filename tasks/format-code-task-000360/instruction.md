## Problem Statement

When I run AllThePlaces spiders for non-US locations, the `phone` field comes out in whatever local formatting the site used, and some perfectly valid international numbers get counted as invalid. Could we make phone output/validation handle real international phone numbers more consistently, so parseable numbers are emitted in a normalized form instead of each spider’s raw formatting?

## Expected outcomes

- Phone normalization:
  - When an item has a parseable valid `phone` value and enough country context is available, the emitted `phone` value should use a consistent international representation rather than preserving arbitrary source formatting.
  - Valid national-format phone numbers for non-US countries should be normalized using their item country context, not treated as US-shaped strings.
  - Existing output continues to use the `phone` field; this change should not require individual spiders to hand-normalize common phone-number formatting variations.

- Phone validation:
  - Valid international or country-local phone numbers should not be counted as invalid merely because they do not match a US-style phone pattern.
  - Phone-like values that are syntactically shaped like a phone number but are not valid real numbers should still be reported through the existing `atp/field/phone/invalid` statistic.

## Implementation notes

- The specific parsing/normalization mechanism, data structures, and where the shared handling is wired into the item-processing flow are implementation choices.
- Prefer a centralized behavior that applies consistently across spiders rather than adding one-off formatting fixes to individual spiders.
- Keep the externally observable contract focused on emitted `phone` values and existing validation statistics.
