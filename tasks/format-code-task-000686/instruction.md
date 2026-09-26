## Service instance response is missing the `service_plan` link

When I fetch a managed service instance via the API, the `links` block in the response doesn't include a link to the service plan it was created from.

Repro:

```
cf create-service my-offering my-plan my-instance
cf service my-instance --guid
# -> <guid>
cf curl /v3/service_instances/<guid>
```

In the returned JSON, under `links` I get `self`, `space`, `credentials`, `service_credential_bindings`, `service_route_bindings` — but there's no entry pointing at the plan. On regular CF this response includes a link that lets you navigate from a service instance to its plan, and tooling I'm porting over relies on following that link to fetch plan details (e.g. to display which plan an instance is on, or to look up plan metadata) without having to know the plan GUID up front.

It would be good for korifi's `/v3/service_instances/<guid>` response to expose the service plan as a link too, so clients can traverse from an instance to its plan the same way they do against cloud_controller.
