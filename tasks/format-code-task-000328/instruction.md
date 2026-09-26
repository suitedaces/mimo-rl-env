# Add a Zenefits source connector

We want a new Airbyte source connector for [Zenefits](https://developers.zenefits.com/), the HR /
people-management platform, so users can replicate their Zenefits data into Airbyte. Please build it
as a Python connector using the repository's connector framework (the Airbyte CDK), following the
same conventions the other Python sources in this repo use.

The connector should be importable as the `source_zenefits` package, and its CDK `AbstractSource`
implementation should be the class `SourceZenefits` (reachable as `source_zenefits.source.SourceZenefits`).

## Configuration

The connector takes a single required config field, `token` — the Bearer token a user generates in
the Zenefits portal. Every request the connector makes to the Zenefits API must be authenticated by
sending this token in an `Authorization: Bearer <token>` HTTP header.

## API shape

All endpoints live under the base URL `https://api.zenefits.com/`. Requests are plain HTTP `GET`s.

A successful list response is an envelope of the form:

```json
{
  "data": {
    "data": [ { ...record... }, { ...record... } ],
    "next_url": "https://api.zenefits.com/core/people?starting_after=<id>"
  }
}
```

- The actual records to emit live under `data.data`.
- `data.next_url` drives pagination: when it is a non-empty URL there is another page to fetch and
  the connector must follow it to retrieve the remaining records; when it is `null`/absent the
  stream is complete. All records across all pages must be emitted, in order.

## Streams

Expose exactly the following 11 full-refresh streams. Each stream's name must be exactly as listed,
and each must read from the given path relative to the base URL:

| stream name           | path                              |
|-----------------------|-----------------------------------|
| `people`              | `core/people`                     |
| `employments`         | `core/employments`                |
| `departments`         | `core/departments`                |
| `locations`           | `core/locations`                  |
| `labor_groups`        | `core/labor_groups`               |
| `labor_group_types`   | `core/labor_group_types`          |
| `custom_fields`       | `core/custom_fields`              |
| `custom_field_values` | `core/custom_field_values`        |
| `vacation_requests`   | `time_off/vacation_requests`      |
| `vacation_types`      | `time_off/vacation_types`         |
| `time_durations`      | `time_attendance/time_durations`  |

`SourceZenefits.streams(config)` must return one stream instance per row above (11 in total).

## Connection check

`SourceZenefits.check_connection(logger, config)` validates the supplied token by making a request
to the Zenefits API. It returns a `(bool, error)` tuple: `(True, None)` when the API responds
successfully, and `(False, <error>)` (a falsy/`None` second element only on success — otherwise a
truthy error object describing the failure) when the request fails, e.g. the token is rejected with
an HTTP error status. It must not raise in that failure case.
