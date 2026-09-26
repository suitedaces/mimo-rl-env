## Problem Statement

I want to be able to run crontabber through the normal `./scripts/socorro crontabber` entry point, including from the Docker scripts, instead of having it be this odd one-off. Also, setting up `crontabber.jobs` is pretty clunky right now; it’d be nice if I could point it at a reusable jobs preset, especially for stage where I need the fake Hive ADI fetch job included.

## Expected outcomes

- Crontabber can be launched through the standard Socorro command-line entry point as `./scripts/socorro crontabber`.
- The Docker helper scripts that start crontabber use the same standard entry point, while preserving the update-data job selections they already pass.
- Existing inline `crontabber.jobs` values continue to work.
- `crontabber.jobs` can also refer to a reusable Python jobs value, including `socorro.cron.crontabber_app.DEFAULT_JOBS`.
- A stage-oriented reusable jobs value is available at `socorro.cron.crontabber_app.STAGE_JOBS`, and it includes the normal crontabber jobs together with the fake Hive ADI fetch job needed for stage.

## Implementation notes

- Preserve existing crontabber job behavior unless it is directly affected by the launcher or jobs configuration changes above.
- The internal parsing structure, helper functions, shell variable names, and configuration wiring are up to the implementer as long as the observable launcher, Docker helper, and `crontabber.jobs` behaviors are satisfied.
