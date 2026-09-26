## `convert_called_station_id` produces noisy ERROR logs and occasionally crashes

We run the `convert_called_station_id` management command on a schedule to fix up Called-Station-IDs by pulling routing info from our OpenVPN management interfaces. A few annoyances we've hit:

### 1. ERROR-level logs for routine connection failures

Our OpenVPN servers occasionally have their management interface unavailable for short periods (restarts, deploys, transient network blips). When that happens the command logs things like:

```
ERROR ... Unable to establish telnet connection to <host> on <port>. Skipping!
ERROR ... Error encountered while connecting to <host>:<port>: ... Skipping!
```

These end up paging our on-call because our alerting treats anything at ERROR level as actionable. But the command is already handling these cases gracefully — it just skips that host and moves on. They really shouldn't be ERROR; a warning would be more appropriate so monitoring doesn't treat a transient telnet failure as a real incident.

### 2. The command sometimes dies in the middle of a run

On some hosts the management command exits abnormally before processing all the configured organizations. From what we can tell it happens when a connection to the OpenVPN management interface gets cut from the remote side rather than refused outright (e.g. the daemon accepts the TCP connection and then closes it). Instead of skipping that host like it does for refused/timed-out connections, the whole command terminates and the remaining organizations don't get processed at all.

It would be great if this case were treated the same way as the other connection failures — log it, skip the host, keep going.

### 3. Deprecation warnings from the logging calls

When the command runs we also see `DeprecationWarning` noise coming from the logging calls inside this command (Python's logging module has deprecated one of the methods being used here). Would be nice to clean that up while you're in there.

Thanks!
