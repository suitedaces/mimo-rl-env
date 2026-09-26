## Feature request: built-in base64 string validator

I'm using Zod to validate API payloads, and a few of my endpoints accept fields that are expected to be base64-encoded strings (think things like binary blobs uploaded as base64, signed tokens, webhook payloads, etc.).

When writing the schema for one of those endpoints, I reached for the obvious thing:

```ts
const Schema = z.object({
  payload: z.string().base64(),
});
```

…and TypeScript immediately complained that `base64` doesn't exist on `ZodString`. Looking at the docs, I see Zod ships built-in string format validators for a bunch of common formats — `email`, `url`, `uuid`, `cuid`, `cuid2`, `ulid`, `ip`, `datetime`, `date`, `time`, etc. — but base64 isn't one of them, which surprised me a bit since it's such a common format on the wire.

Right now my workaround is to drop down to a `.refine()` with a hand-rolled regex, but that means:

- Every project I work on ends up with its own slightly-different base64 regex copy-pasted in.
- The resulting `ZodIssue` doesn't look like the ones from the other built-in string formats (different `code` / `validation` shape), so my shared error-formatting / i18n layer has to special-case it.

It feels pretty natural for this to live alongside the other string format validators in core Zod. Would you accept a PR that adds `z.string().base64()` as a first-class string validator, behaving consistently with the existing ones (chainable on `ZodString`, accepts an optional custom error message, fails with a regular `ZodError` whose issue is shaped like the other string-format issues)?

Happy to put up the PR if you're open to it.
