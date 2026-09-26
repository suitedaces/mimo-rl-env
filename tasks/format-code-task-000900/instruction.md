I'm running a backend group with `consensus_aware = true` and three upstreams, and even when all three are healthy and in agreement, almost all RPC traffic lands on the first backend in the config. If I mark that first one unhealthy, I still see requests hit it and fail before falling through, and a degraded backend near the top of the list also gets picked before the other healthy nodes. I'm not sure if my config is wrong, but consensus-aware routing looks like it's just following the config order instead of the current backend state.

Expected outcomes:
- For a backend group configured with `consensus_aware = true`, RPC forwarding should use the currently agreed consensus set rather than simply walking the original configured backend order.
- When multiple healthy, non-degraded upstreams are in the current consensus set, repeated stable traffic should be observable across more than one of those upstreams instead of consistently concentrating on the first configured backend.
- Upstreams that are currently unhealthy should not be selected for normal forwarding in a consensus-aware backend group; if other healthy consensus members are available, requests should go to those members without first failing against the unhealthy one.
- Healthy but degraded upstreams may still be used as fallback candidates, but healthy non-degraded upstreams should be preferred ahead of degraded ones.

Implementation notes:
- The routing mechanism, data structures, and exact place where candidates are selected are up to the implementation.
- Preserve existing consensus-aware semantics outside of backend candidate selection, including normal request handling and fallback behavior when no suitable backend is available.
