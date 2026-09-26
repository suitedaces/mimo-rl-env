# Add a read API for model stages

Our backend already persists **model stages** — each one is a named checkpoint that
belongs to a model (the stage carries a `name`, a `timestamp`, an optional `map`
score, and the id of the model it belongs to). The database table and ORM model are
already in place, but there is currently no HTTP API to look a stage up, and nothing
guards against stages whose names are malformed. We need to expose model stages over
the same versioned REST API the rest of the app uses (`/api/v1`).

Please add a read API for model stages, mounted under `/api/v1/model_stages`, with the
following behaviour. Like the other resource endpoints, these require an authenticated
active user.

## Fetch a single stage

`GET /api/v1/model_stages/{stage_id}` returns the stage wrapped in the usual envelope:

```json
{"result": { ...stage fields... }}
```

The returned stage must expose at least its `id`, `name`, `map`, and `model_id`, plus a
nested `model` object exposing the owning model's `id` and `hash`.

- If no stage has that id, the request fails as *not found* (HTTP 404) and the response
  body carries the error code **112001**.

## Validate stage names on lookup

A stage name is only considered valid when it is a non-empty string that forms a valid
identifier: it starts with a letter or an underscore and contains only letters, digits,
and underscores (e.g. `best`, `stage_1`, `_tmp` are valid; `""`, `1stage`, `with space`,
`a-b` are not).

When a single stage is fetched by id and its stored name is not valid, the request must
fail with the error code **112002** (a distinct outcome from the not-found case above),
rather than returning the stage.

## Fetch several stages at once

`GET /api/v1/model_stages/batch?ids=1,2,3` returns

```json
{"result": [ ...stages... ]}
```

containing exactly the stages whose ids exist, in any order; ids that match no stage are
simply omitted (an all-missing request yields an empty list). This batch endpoint returns
the matching stages without rejecting the request.
