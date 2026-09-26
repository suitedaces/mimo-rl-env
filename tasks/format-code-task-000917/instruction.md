## `to-json-schema` doesn't support common string validation actions

I'm using `@valibot/to-json-schema` to generate a JSON Schema from my Valibot schemas (so I can feed it to a form generator / OpenAPI doc). A bunch of very common string validations don't make it through the conversion.

Example:

```ts
import * as v from 'valibot';
import { toJsonSchema } from '@valibot/to-json-schema';

const Color = v.pipe(v.string(), v.hexColor());
const Id    = v.pipe(v.string(), v.ulid());
const Code  = v.pipe(v.string(), v.digits());
const Tag   = v.pipe(v.string(), v.emoji());
const Empty = v.pipe(v.string(), v.empty());

toJsonSchema(Color); // ⚠️ action cannot be converted to JSON Schema
toJsonSchema(Id);    // ⚠️ action cannot be converted to JSON Schema
// ...same for digits, emoji, empty, and several others
```

The actions I've hit so far that aren't handled:

- `bic`
- `cuid2`
- `decimal`
- `digits`
- `emoji`
- `empty`
- `hexadecimal`
- `hexColor`
- `nanoid`
- `octal`
- `ulid`

All of these are basic string format validators (most of them are just a regex under the hood) so I'd expect them to round-trip into JSON Schema the same way `email`, `uuid`, `iso_date` etc. already do. Right now I have to strip them out of my pipelines or wrap them in raw `v.regex(...)` calls before passing to `toJsonSchema`, which defeats the point of having named actions.

Could support for these actions be added so the resulting JSON Schema still carries the validation constraint?
