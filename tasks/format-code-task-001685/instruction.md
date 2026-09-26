Add a fallback mechanism to look for KeptnEvaluationDefinitions
## Goal

KLT fallbacks to search for a `KeptnEvaluationDefinition` in the namespace in which it's deployed if it cannot find it in the namespace of the `KeptnApp`

## Technical details

Currently, KLT only looks for `KeptnEvaluationDefinition` in the same namespace in which the `KeptnApp` is defined. If the task is not found, it will stop with an error. We should provide a fallback to look into the same namespace in which KLT is deployed. If a task is found there, it will be executed. Otherwise, it will stop the deployment with an error.

## DoD

- [x] Unit tests
- [x] KLT has a fallback search for `KeptnEvaluationDefinition` in its namespace
- [x] documentation adapted
