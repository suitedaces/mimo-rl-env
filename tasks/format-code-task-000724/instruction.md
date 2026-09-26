# Problem Statement

我想通过 REST API 动态改某个 db 的 audit 配置，按理说 PUT/POST `/{db}/_config/audit` 应该能做这事吧？但我试了下，不管发什么请求体过去，配置都没变，GET 回来还是原样，感觉这俩接口压根没接上。能不能让 PUT 整体替换、POST 增量改 audit events 真正生效？另外 GET 现在直接返回一坨 events map，我想顺便知道 audit 整体是不是开着的，最好能把全局 enabled 也带出来。

# Expected outcomes

- `GET /{db}/_config/audit` returns a JSON object that includes both the database audit enabled state and the audit event configuration, rather than returning the event map as the top-level response.
- The audit enabled state and event enabled states returned by `GET /{db}/_config/audit` reflect the current persisted database configuration after defaults/runtime configuration are applied, including changes made through the configuration API without requiring a database restart.
- `GET /{db}/_config/audit` includes an ETag corresponding to the current database configuration version when the audit configuration is available.
- If database audit configuration cannot be read because the server is running without persistent configuration support, `GET /{db}/_config/audit` returns a `503 Service Unavailable` response with an audit-configuration-unavailable error.
- `PUT /{db}/_config/audit` treats the request body as a full replacement of the database audit configuration: the global audit enabled value is replaced from the request body, and the enabled event set is rebuilt from the events explicitly enabled in the request.
- `POST /{db}/_config/audit` treats the request body as an incremental update: explicitly supplied global audit enabled values are updated, events set to enabled are added, events set to disabled are removed, and omitted fields/events are left unchanged.
- `PUT /{db}/_config/audit` and `POST /{db}/_config/audit` reject malformed or unknown audit event IDs in the submitted events object with a `400 Bad Request` response that identifies the audit configuration update failure and distinguishes invalid event ID syntax from unknown event IDs.
- When `GET /{db}/_config/audit` is requested in verbose form, each event entry includes the available event metadata and enabled/filterable state using the documented event object fields, while omitting unavailable metadata fields from the JSON response.

# Implementation notes

The implementation may choose where to perform parsing, validation, persistence updates, and response construction, as long as the externally observable REST API behavior above is satisfied. Keep the behavior compatible with existing audit event identifiers and existing admin API conventions for JSON responses, errors, and configuration versioning.
