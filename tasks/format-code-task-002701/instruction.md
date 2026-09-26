# Problem Statement

When I use a CPU_Multicore Map in DaCe, the generated C++ just has a bare `#pragma omp parallel for` and I can't seem to control the OpenMP scheduling at all. For some of my kernels static scheduling tanks performance and I really want dynamic or guided with a chunk size, plus the ability to cap the thread count for a specific map. Could you add a way to set the schedule kind, chunk size, and num_threads per map so it actually shows up in the emitted pragma?

# Expected outcomes

- DaCe provides a public OpenMP schedule-kind API for maps, exposed as `dace.dtypes.OMPScheduleType`, covering the default/no-override behavior and common OpenMP schedule kinds such as static, dynamic, and guided.
- Map objects expose public per-map controls named `omp_schedule`, `omp_chunk_size`, and `omp_num_threads`, usable when a map is scheduled as `dace.dtypes.ScheduleType.CPU_Multicore`.
- With the OpenMP-specific map controls left at their defaults, generated C++ for a CPU multicore map remains compatible with previous output and does not add scheduling or thread-count clauses to the OpenMP parallel-for pragma.
- When those per-map controls request an OpenMP schedule, a positive chunk size, and/or a positive thread count, the generated CPU multicore parallel-for pragma reflects the requested OpenMP `schedule(...)` and `num_threads(...)` clauses. Unset or non-positive chunk/thread values should not request extra clause arguments.

# Implementation notes

- Preserve existing CPU multicore map behavior unless the new OpenMP-specific map settings are explicitly used.
- The exact internal representation, validation location, serialization details, and code organization are up to the implementer, as long as the public map controls and generated C++ behavior above are satisfied.
- Do not change the semantics of non-CPU-multicore maps while adding these controls.
