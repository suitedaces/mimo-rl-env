I’m trying to validate a password-change struct and make sure `NewPassword` isn’t the same as `OldPassword`, but `validate:"unique=OldPassword"` doesn’t seem to work on regular fields and just blows up. It’d be really nice if `unique` could compare against another field in the same struct for cases like this.

Expected outcomes:
- When `unique=<FieldName>` is used on a regular non-collection field inside a struct, it should compare the current field with the named sibling field in that same struct: different values pass validation, and equal values fail validation for the current field.
- If the sibling-field comparison cannot be performed because the tag does not identify a usable same-struct field, validation should panic rather than silently passing or returning a normal validation error.

Implementation notes:
The internal comparison path, reflection organization, and where the panic is raised are up to the implementation. The observable contract is the struct validation result and panic behavior described above.
