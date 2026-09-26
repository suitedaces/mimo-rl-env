## Stale gating in `.buildkite/gen-pipeline.sh` should be cleaned up

While looking at the Buildkite pipeline generation script, I noticed a couple of conditional checks in there that no longer reflect the current test matrix and the current testing scope.

**1. Dead Python 3 gating around the Elastic tests**

In `run_gloo_integration`, the Elastic test block is wrapped in a check that only schedules the tests when the test name implies Python 3. Every test configuration we still maintain in the `tests=( ... )` array at the top of the script already targets Python 3, so this guard never evaluates to false anymore — it's just dead code that makes the function harder to read. The Elastic tests should simply run for every gloo configuration unconditionally.

**2. Spark integration tests are skipped on pure-gloo configurations**

In `run_spark_integration`, several test commands (the Spark Keras Rossmann Run/Estimator, Spark Keras MNIST, and Spark Torch MNIST) are wrapped in a guard that excludes test configurations whose name contains `gloo` unless it also contains `openmpi-gloo`. The original intent seems to have been "don't run these on gloo-only setups," but Spark integration on gloo is something we want to cover going forward. These Spark example runs should execute on the gloo-only configurations as well, just like they already do on the mixed/openmpi setups.

Could we drop both of these stale conditions so the pipeline reflects what we actually want to run? The other surrounding conditions (e.g. the TF1 / `tf2` / `torch0_` / `mpich` / `oneccl` exclusions in `run_spark_integration`, the GPU-queue guard around `test_spark_keras.py` / `test_spark_torch.py`) should stay as they are — only the two gates described above are stale.
