## VM query endpoint fails when the queried function produces log entries

I'm using the node's VM query API (POST `/vm-values/query`) to call view-style functions on a deployed smart contract. Most queries work fine, but one particular query consistently fails — that function happens to emit an event during its execution.

If I point the same query endpoint at a different function on the same contract that doesn't produce any log entries, the response comes back normally with return data, gas remaining, output accounts, etc. As soon as the executed function produces at least one log entry, the request never returns successfully — I get a server error back instead of a payload.

This is reproducible enough that I'm fairly sure it's not specific to my contract: any contract whose call produces a non-empty list of log entries triggers it. A SC call that returns zero logs round-trips fine.

What I'd expect: the API should return the full VM output regardless of whether the execution emitted logs. The `Logs` array on `VMOutputApi` exists for exactly this purpose, and right now there seems to be no way for a query that actually produces logs to reach the client through this endpoint.

Repro:
- Deploy any contract with a function that emits one or more events during execution.
- Send a `vm-values/query` request targeting that function.
- The request errors out instead of returning the VM output with the logs included.
