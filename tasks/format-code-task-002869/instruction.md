## Feature request: way to query the current number of connected clients

I'm running a Pitaya v2 game server and I'd like to publish a "currently connected clients" gauge to our monitoring stack. Use cases on my side are pretty mundane — an HTTP handler on the admin port that returns server stats, plus a periodic metric exporter that pushes the value to Prometheus.

Looking at the top-level `session` package I see helpers like `session.GetSessionByUID`, `session.GetSessionByID`, `session.OnSessionBind`, `session.OnSessionClose`, `session.CloseAll` — but I can't find anything that just answers "how many clients are connected right now?" from this entry point.

The closest workaround I have right now is to register `OnSessionBind` and `OnSessionClose` callbacks and maintain my own atomic counter. That works, but it feels redundant: the framework already has to track connected sessions internally (otherwise `CloseAll` wouldn't be able to iterate them and report progress in its log line). Forcing every user to re-do that bookkeeping outside the library seems unnecessary.

Could the `session` package expose a public helper that I can call from anywhere in my app to get the current connected-client count, without me having to plug into the bind/close callbacks? Something like `GetNumberOfConnectedClients()` returning an `int64` would work for me.
