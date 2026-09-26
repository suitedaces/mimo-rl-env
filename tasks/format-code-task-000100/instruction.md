## Splitting a benchmark across `--run_stage=prepare` and `--run_stage=run` fails when a flag default uses Pint units

I'm trying to run a benchmark in two phases by invoking PerfKitBenchmarker once with `--run_stage=prepare` and then again with `--run_stage=run`, so that the pickled state from the prepare phase is picked up by the run phase.

This works for plain benchmarks, but as soon as the benchmark declares a flag whose default value is a Pint quantity (using `UNIT_REGISTRY` from `perfkitbenchmarker`) and I don't explicitly override it on the command line, the run phase blows up while loading the saved state. If I override the same flag on the command line so the default is never pickled, the two-stage run goes through fine.

It looks like quantities created against the prepare phase's `UNIT_REGISTRY` don't survive a round-trip through pickle into the run phase, which has its own registry instance. For users this is pretty surprising — the default value of a flag shouldn't break `--run_stage` separation just because it carries units.

Could `perfkitbenchmarker` make Pint quantities safe to pickle/unpickle so that the prepare/run split works regardless of whether a units flag uses its default?
