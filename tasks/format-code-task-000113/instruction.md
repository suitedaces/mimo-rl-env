## Job logs stop being written after a single write failure

I'm running jobs through mist and reading their logs via the async log streaming. For most jobs this works fine, but every once in a while I notice that a job's log file just stops growing partway through the job — even though the job itself keeps running and producing output. When I look later, the tail of the log for that job is just missing.

After staring at this for a while I think I've narrowed it down to what happens when writing a batch of log events fails once (e.g. a transient IO hiccup on the log directory, or anything that makes `LogsWriter.write` fail for a single batch). From that point on, no further log events for that job make it to disk — it's as if the per-job log pipeline is shut down by the first failure and never recovers, even though new `LogEvent`s are still arriving for the same job.

The expected behavior is that a single failed write shouldn't kill log storage for that job. If one batch fails, fine — drop/skip that batch, but subsequent batches for the same job should still be written and still produce update events for the async consumers. Right now one bad batch effectively blackholes all remaining logs for that job until the job finishes.

This is happening in the `storeFlow` in `LogStreams` (the `mapAsync` that calls `writer.write(jobId, events)`), if that helps narrow it down.
