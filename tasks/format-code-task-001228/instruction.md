## Rename `CountsPredictor` and modernize its API for consistency with `MapEvaluator`

Right now we have two classes that essentially do the same job — compute predicted counts (`npred`) from a model and a set of IRFs — but they're inconsistent:

- In the `map` package we have `MapEvaluator`, which exposes a single method that returns the predicted counts directly.
- In the `spectrum` package we have `CountsPredictor`, with a clunky two-step usage pattern:

```python
predictor = CountsPredictor(model=model, aeff=aeff, edisp=edisp, livetime=livetime)
predictor.run()
result = predictor.npred
```

You have to remember to call `run()` first, and the result lives on a `.npred` attribute rather than being returned. That's awkward, and the name `CountsPredictor` doesn't line up with the `*Evaluator` naming used on the map side.

### Proposal

Bring the spectrum-side class in line with `MapEvaluator`:

1. Rename the class so its name matches the `*Evaluator` style used elsewhere for the equivalent map-side functionality.
2. Replace the `run()` + `.npred` attribute pattern with a single method call that computes and **returns** the predicted `CountsSpectrum` directly, so callers can write something like:

   ```python
   result = evaluator.<single_call>(...)
   ```

   instead of needing two separate steps.

All the existing constructor arguments (`model`, `aeff`, `edisp`, `livetime`, `e_true`) should keep working the same way; only the class name and the way you trigger the computation / get the result need to change.

### Callers to update

There are several places inside gammapy that currently use `CountsPredictor` via the old two-step pattern and need to be migrated to the new API:

- `gammapy/spectrum/fit.py` (used inside `SpectrumDataset` and `SpectrumFit._predict_counts_helper`)
- `gammapy/spectrum/observation.py` (`SpectrumObservation.predicted_counts`)
- `gammapy/spectrum/simulation.py` (`SpectrumSimulation.npred_source` / `npred_background`)
- `gammapy/spectrum/sensitivity.py` (`SensitivityEstimator.run`)
- `gammapy/time/lightcurve.py` (`LightCurveEstimator.compute_flux_point`)

And of course `__all__` / docstrings / the example in the class docstring should be updated to reflect the new name and usage.

This is the implementation of the proposed change PR 12 from PIG 7.
