I have some batch jobs where I need a final cleanup/notification job to run after the rest of the pipeline is done, even if one of the parent jobs fails or gets cancelled. Right now dependent jobs just get cancelled in that case, so I don't have a good way to reliably release resources or send failure notifications from Batch itself. Could there be a way to mark a child job as “run anyway after its parents finish”?

Expected outcomes:
- Public job creation supports an optional boolean opt-in named `always_run` for dependent jobs.
- When the opt-in is enabled for a dependent job, the Batch service accepts the request and remembers that setting for that job.
- A marked dependent job waits until its parents have finished, then can run even when a parent did not finish successfully.
- Existing dependency behavior remains the default: jobs that do not opt in, including jobs created with `always_run=False`, are still prevented from running when a parent does not finish successfully.

Implementation notes:
- The exact internal representation, validation location, and scheduling mechanism are up to the implementation.
- Preserve existing job creation behavior for callers that do not opt in to this setting.
