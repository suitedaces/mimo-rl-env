## Members content gating doesn't respect a post's `visibility` setting

I'm running Ghost with the `members` labs flag enabled. Posts in the admin UI already have a **visibility** field that can be set to `public`, `members`, or `paid`, and I want to use that to control who can read each post:

- `public` — anyone can read it
- `members` — only signed-in members can read the content
- `paid` — only members with an active paid subscription can read the content

In practice the visibility setting doesn't seem to do anything for me. Whether I switch a post between `public`, `members`, and `paid`, the API still returns the same `plaintext` / `html` to the same caller. The only way I've found to actually hide post content from non-members is to attach a specific tag to the post, which is awkward (it shows up on the post like any other tag) and also can't express the difference between "members" and "paid" — a free signed-in member ends up seeing paid posts just like a paying one does.

It would be much nicer if the post serializer used the `visibility` field directly. Roughly the behaviour I'd expect:

| visibility | anonymous request | signed-in free member | signed-in paying member |
|---|---|---|---|
| `public`  | content returned | content returned | content returned |
| `members` | content hidden   | content returned | content returned |
| `paid`    | content hidden   | content hidden   | content returned |

This should apply to both the v2 and canary Content APIs, and it should only kick in when the `members` labs flag is on (so existing sites without members enabled keep behaving exactly as they do today).
