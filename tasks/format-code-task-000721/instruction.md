## Problem Statement

I turned on resource monitoring with `MonitoredResources` set to track heap, but the heap utilization always reads as 0 even when the process is clearly using a lot of memory, so the heap-based limiting never kicks in. On top of that, I'm scraping `/metrics` and I see `cortex_resource_based_limiter_limit` only carries a `component` label — when I configure both cpu and heap on the same component I can't tell which limit belongs to which resource, they look like they're stomping on each other. I also tried putting a resource name that isn't cpu or heap in the config just to test and it started up fine without complaining, which felt off. Can you take a look?

## Expected outcomes

- Resource monitoring should report heap utilization from the process's actual heap usage rather than remaining at zero or otherwise unusable when heap monitoring is enabled.
- Heap-based resource limiting should be able to make decisions from the reported heap utilization, so configured heap limits are not silently ineffective.
- The `cortex_resource_based_limiter_limit` metric should distinguish limits for different monitored resources on the same component, including separate cpu and heap entries.
- Configuring an unsupported monitored resource name should fail startup/configuration with a clear error identifying the unknown resource.
- Leaving monitored resources unset or effectively empty should continue to skip resource monitor initialization without error.
- Enabling resource monitoring and allowing it to run should not panic while recording resource utilization.

## Implementation notes

- The exact validation location, data structures, and internal monitor/limiter organization are up to the implementer.
- Prefer externally observable behavior for validation: configuration outcomes, exported metrics, resource utilization behavior, and absence of runtime panics.
- Keep existing supported resource names and existing public configuration/metric surfaces compatible while fixing the incorrect behavior.
