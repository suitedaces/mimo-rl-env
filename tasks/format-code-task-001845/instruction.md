## Problem Statement

I’m using DRF 3.1 with a viewset that has `pagination_class` set, and the list endpoint is paginated at runtime, but the generated Swagger docs don’t show the `page` or page-size query parameters at all. I first thought I had misconfigured the paginator, but the API response is definitely paginated; it’s just missing from the operation parameters in the docs.

## Expected outcomes

- For affected DRF versions using class-based pagination configuration, an enabled paginated list operation should expose the paginator’s configured page query control in the generated Swagger operation parameters.
- If that paginator also allows clients to control page size through a configured query parameter, the generated list operation should expose that page-size control as well.
- Pagination controls emitted for this case should appear as integer Swagger query parameters, consistent with the existing operation-parameter output shape.
- Viewsets without enabled pagination should not gain pagination query parameters solely from this change.
- Existing generated documentation behavior outside this pagination-docs case should remain compatible.

## Implementation notes

- The concrete implementation path, helper structure, and compatibility checks are up to the implementer.
- Preserve the existing public Swagger output shape while extending it to reflect class-based pagination configuration.
- Avoid changing unrelated generated documentation behavior.
