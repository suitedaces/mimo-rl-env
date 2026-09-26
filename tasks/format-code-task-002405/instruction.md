## Problem Statement

Right now when I create a ServiceLevelObjective, the generated recording/alerting rules don't carry any partial response strategy, so my ThanosRuler just falls back to its own default behavior and I can't influence it per-SLO. I'd really like to be able to set the partial response strategy (like abort or warn) on the SLO itself and have it flow through to all the generated rule groups. Ideally it would default to abort if I don't set anything, so existing SLOs keep behaving the same.

## Expected outcomes

- ServiceLevelObjective configuration accepts a per-SLO `spec.partial_response_strategy` setting.
- The new setting is optional and defaults to `abort` when it is not explicitly set.
- ServiceLevelObjective validation accepts the supported partial response strategies, including `abort` and `warn`, and rejects unsupported values.
- Generated recording and alerting rule groups include the ServiceLevelObjective’s configured partial response strategy.
- Both generated Kubernetes rule resources and generated rule YAML carry the configured strategy consistently across all rule groups.

## Implementation notes

- Keep the behavior compatible with existing ServiceLevelObjective resources that do not set the new option.
- The exact implementation location and internal data flow are up to you; focus on the public ServiceLevelObjective API and the externally visible generated rule output.
- Avoid changing unrelated rule generation behavior while adding this configuration option.
