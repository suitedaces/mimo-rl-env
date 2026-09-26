# Add a reusable Amber NVE benchmark test to the test library

Our portability test library (`hpctestlib`) should ship a ready-to-use, site-agnostic
regression test for the [Amber](https://ambermd.org/) molecular-dynamics suite, so that
individual sites can subclass it and only add their machine-specific bits (modules,
valid systems, references, task counts).

Add a run-only regression test class importable as:

```python
from hpctestlib.apps.amber.nve import amber_nve_check
```

It encodes the Amber NVE production benchmarks and must behave as follows.

## Parametrization

The test is parametrized over two independent axes, producing one instance per
combination (8 in total):

* the **benchmark**, one of:
  `Cellulose_production_NVE`, `FactorIX_production_NVE`,
  `JAC_production_NVE_4fs`, `JAC_production_NVE`;
* the **variant** of the code: `mpi` or `cuda`.

Each instance must expose, as readable attributes, the `benchmark` name and the
`variant` it represents.

## Per-variant tooling

Depending on the variant, each instance runs a different executable with a
different input deck:

* `mpi`  → executable `pmemd.MPI`, input file `mdin.CPU`;
* `cuda` → executable `pmemd.cuda.MPI`, input file `mdin.GPU`.

The output file defaults to `amber.out`. The program is always invoked in
overwrite mode reading the input deck and writing the output file, i.e. the
command-line options are exactly `['-O', '-i', <input_file>, '-o', <output_file>]`.

## Task count

The number of MPI tasks is intentionally **not** decided by this base test — it
depends on the target machine. Leave `num_tasks` as a *required* variable that a
subclass (or the user) must set; accessing it before it has been set must raise.

## Tags

Every instance carries the tags `{'sciapp', 'chemistry'}`.

## Validation (sanity)

A run is considered successful only if **both** of the following hold against the
output file:

1. the simulation completed — the output contains the line marker
   `Final Performance Info:`;
2. the computed average total energy is within tolerance of the benchmark's
   reference energy. The validated energy is the **second-to-last** `Etot` value
   reported in the output (the average over the run, as opposed to the trailing
   RMS-fluctuation value). Validation passes when
   `abs(energy - reference) < abs(reference * tolerance)`.

The reference energy and relative tolerance are specific to each benchmark:

| benchmark                  | reference energy | tolerance |
|----------------------------|------------------|-----------|
| `Cellulose_production_NVE` | `-443246.0`      | `5.0e-05` |
| `FactorIX_production_NVE`  | `-234188.0`      | `1.0e-04` |
| `JAC_production_NVE_4fs`   | `-44810.0`       | `1.0e-03` |
| `JAC_production_NVE`       | `-58138.0`       | `5.0e-04` |

If either condition fails, the sanity stage must fail.

## Performance

The test reports a single performance metric expressed in `ns/day`, extracted
from the output line of the form `ns/day = <value>`.
