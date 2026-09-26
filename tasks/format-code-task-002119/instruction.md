k8sclusterreceiver pod and container metadata.yaml break CI
@dmitryax @atoulme heads up that CI is [broken](https://github.com/open-telemetry/opentelemetry-collector-contrib/actions/runs/5392516937/jobs/9790995716) on `main` after #23783 got merged, because for the changes in this PR (which weren't included in the branch from #23783) the new `metadata.yaml`:
- don't have the parent field
- some metrics are missing units.

Let me know if you would like to add the PR to add the parent + units, otherwise I can put this up ?

_Originally posted by @mackjmr in https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/23441#issuecomment-1609933209_
