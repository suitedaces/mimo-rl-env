# Render a list of GitHub deployments as a Slack message

We want to show a repository's GitHub deployments inside Slack. The data comes from
GitHub's GraphQL API as an array of deployment nodes, each shaped like:

```js
{
  creator:     { login, url, avatarUrl },
  ref:         { name },
  commit:      { message, abbreviatedOid, commitUrl },
  description: <string|null>,
  task:        <string>,        // e.g. "deploy"
  environment: <string>,        // e.g. "production"
  state:       <string>,        // a GitHub deployment state, see below
  createdAt:   <ISO-8601 string>,
  latestStatus: { state, description } | null
}
```

Add a new message renderer, available as the default export of
`lib/messages/deployment-list.js`, that follows the same convention as the other
renderers in that directory: it is constructed with the array of deployment nodes and
exposes a `toJSON()` method that returns the Slack message payload.

`toJSON()` must return an object of the form `{ attachments: [...] }` containing exactly
one attachment per deployment, in the same order as the input array. An empty input array
yields `{ attachments: [] }`.

Each attachment must contain:

- `fallback`: the plain-text summary `"<login> triggered a <task> on <environment> from <ref name>"`,
  where `<login>` is the creator's login and `<ref name>` is `ref.name`.
- `color`: a hex color derived from the deployment `state` (see mapping below).
- `pretext`: the deployment `description` (omit it when the description is null/empty).
- `author_name`: the creator's login.
- `author_link`: the creator's `url`.
- `author_icon`: the creator's `avatarUrl`.
- `title`: `"<ref name> <commit message>"`.
- `title_link`: `commit.commitUrl`.
- `fields`: a list of short fields (each `{ title, value, short: true }`) in this order:
  `Task` (the task), `Environment` (the environment) and `State` (the state). When the
  deployment has a `latestStatus`, append one more short field titled `Latest Status`
  whose value is `"<status state> <status description>"`. When `latestStatus` is null, no
  such field is present.
- `footer`: the literal string `"Created"`.
- `footer_icon`: `"https://assets-cdn.github.com/favicon.ico"`.
- `ts`: the `createdAt` timestamp expressed as Unix seconds (i.e. milliseconds since the
  epoch divided by 1000).

Color mapping from deployment state (use the project's existing palette constants where
they match these hex values):

| state       | color     |
|-------------|-----------|
| `ABANDONED` | `#24292f` |
| `ACTIVE`    | `#36a64f` |
| `DESTROYED` | `#cb2431` |
| `ERROR`     | `#cb2431` |
| `FAILURE`   | `#cb2431` |
| `INACTIVE`  | `#24292f` |
| `PENDING`   | `#dbab09` |
