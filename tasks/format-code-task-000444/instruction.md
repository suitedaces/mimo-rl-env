## Time to refresh the CI setup

The `.github/workflows/pre-commit.yml` workflow and the pre-commit config are starting to feel out of date and the test suite is needlessly slow / network-dependent. Filing this so we don't lose track. Concretely:

**Stale CI dependencies.** The workflow is still pinned to old major versions of the standard GitHub Actions (checkout etc.), and the pre-commit hook revs (black, isort, the built-in hooks repo) have all gone through several releases since the versions we have committed. We should bump them and re-run the formatters, which will probably cause a small amount of churn in the codebase as the newer black makes slightly different formatting choices.

**Python version matrix.** We're still testing against 3.9 in the matrix even though it's basically at end of life, and we're not testing against 3.12 at all. Time to drop the old one and add the new one. The package metadata should also be updated to reflect the minimum supported Python.

**Tests reach out to the network.** Several tests load `gpt2` from HuggingFace as a small "real" model to exercise the merging machinery. This has two annoying consequences:
- CI runs spend non-trivial time downloading the weights on every fresh runner.
- On a developer machine without network access (planes, locked-down corp networks, etc.) the test suite just fails to start.

Since these tests don't actually care about the *values* in the weights — they only care that the architecture is exercised end-to-end — we don't need the real pretrained checkpoint. They should be reworked to use a small in-process model with the same architecture so no network is required to run `pytest`.

While doing the above we may also want to clean up a couple of harmless warnings that show up in the test output and add a couple of additional sanity-check pre-commit hooks for the non-Python config files we have in the repo.
