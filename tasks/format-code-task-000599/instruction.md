## Allow hooks to skip checkout by clearing `BUILDKITE_REPO`

### Use case

We have a few buildkite pipelines that don't actually need source code—things like deployment jobs, maintenance tasks that hit external APIs, jobs that just orchestrate other jobs, etc. For those, doing a full git clone is pointless and just slows things down.

What I'd like to do is decide in a hook (typically `environment`) whether the job needs source for this particular run, and if not, skip checkout entirely. The most natural way to express that is from the hook itself, e.g. something like:

```bash
# .buildkite/hooks/environment
if [[ "$BUILDKITE_PIPELINE_SLUG" == "deploy-prod" ]]; then
  export BUILDKITE_REPO=""
fi
```

### What actually happens

Clearing or unsetting `BUILDKITE_REPO` from a hook doesn't skip checkout—the agent still goes into the checkout phase and tries to clone, which then fails (since there's no repo URL to clone from) and the whole job errors out before the command phase ever runs.

### What I'd expect

If `BUILDKITE_REPO` ends up empty by the time the checkout phase starts, the agent should just skip checkout and continue on to run the command. The command still needs somewhere reasonable to execute from, so the working directory should be set up sensibly even when nothing was checked out (and ideally cleaned up afterwards so we don't leak directories on the agent host across many such jobs).

This would let people opt individual jobs out of checkout from a hook, without having to maintain a separate agent / queue / pipeline config for "no-checkout" jobs.
