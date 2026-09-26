## Problem Statement

When I define a `ModelViewSet`, I instinctively want to set `model = Department`, but it looks like the CRUD routes only recognize `model_class` right now. Could you make `model` work there instead, including for the base viewset?

## Expected outcomes

- `ModelViewSet` subclasses can declare their Django model with a public `model` class attribute, and registered CRUD routes use that model for their default list, create, retrieve, update, and delete behavior.
- `BaseModelViewSet` subclasses can also declare their Django model with a public `model` class attribute, with the same effect when routes are registered.
- Existing public examples, documentation, and test-facing usage for model-backed viewsets should demonstrate `model = Department`-style configuration rather than the older `model_class` spelling.
- Validation and route registration should continue to fail appropriately when a viewset does not provide a usable Django model configuration.

## Implementation notes

- The exact internal validation flow and how view instances receive the configured model are implementation details.
- Keep the public API focused on declaring the model through the viewset class attribute; avoid requiring callers to pass the model separately when registering normal CRUD routes.
