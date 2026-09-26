## Problem Statement

I'm seeing my webhook receiver choke on the timestamp field in NetBox payloads — it's coming through as `2023-11-29 12:34:56.789012+00:00` with a space between the date and time, and my parser expects something it can read as a proper datetime. Also noticed something weird in the ASN list: when I sort by the ASDOT column I get 1.0, 10.0, 2.0 instead of actual numeric order. And separately, I can create two managed files pointing at the exact same path without any complaint, which feels like it shouldn't just silently go through.

## Expected outcomes

- Webhook payload timestamps:
  - Any webhook payload timestamp emitted by NetBox should be serialized in a standard machine-parseable datetime format with an ISO-style date/time separator rather than a space.

- ASN ASDOT ordering:
  - Sorting the ASN list/table by the ASDOT column should order rows according to the numeric ASN value, not lexicographically by the displayed ASDOT text.

- Managed file path uniqueness:
  - Managed files should not allow two saved records to refer to the same file root and file path combination.
  - Attempting to save a duplicate managed file path should fail with a validation error that clearly identifies the duplicate managed file path.

## Implementation notes

The exact implementation approach, validation location, and internal data structures are up to the implementer. Preserve existing public behavior except where needed to make webhook timestamp serialization, ASDOT sorting, and managed file duplicate-path validation match the outcomes above.
