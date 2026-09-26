I’m using `parseBody()` with forms that send field names like `user.name` and `user.email`, and I’d like to be able to get those back as a nested `user` object instead of flat keys that I have to post-process myself. An optional way to have it understand dot notation would make this much nicer.

Expected outcomes:
- Dot-notation parsing is opt-in: `parseBody(request, { dot: true })` and the request-context parsing API should interpret form field names containing `.` as nested object paths for both `multipart/form-data` and `application/x-www-form-urlencoded` requests.
- Existing behavior remains the default: calls without `dot`, with `dot: false`, or with only existing options should keep dotted field names as flat keys.
- The new dot-notation behavior composes with existing multi-value parsing: when `all: true` or the existing `[]` field-name convention produces an array, that value should appear at the nested path when `dot: true` is also used.
- Returned body containers, including containers created for nested paths, should not inherit from `Object.prototype`, so field names that overlap inherited `Object` properties are handled as form data rather than prototype properties.
- The exported TypeScript API should allow callers to pass the new `dot` option through `ParseBodyOptions`, and `BodyData` should be able to represent nested parsed form data.

Implementation notes:
- The concrete parsing structure, helper functions, and validation location are up to the implementation.
- Preserve compatibility for existing `parseBody()` callers and existing `all` behavior while adding the optional dot-notation mode.
- Keep the behavior consistent across the package entry points that expose the body parsing utility.
