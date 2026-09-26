## RUM events being ingested without a `sessionId`

While looking at the RUM events our app sends to the Datadog intake, I noticed a non-trivial number of them are missing a `sessionId` (the field is just absent / undefined on the event). These same events still have a view id and look otherwise valid, they just have no session attached, which makes them useless for session-level analysis.

After some digging I managed to reproduce it with the following setup:

1. Open our app in two tabs, both initialized with the browser RUM SDK. The session is initially **not** sampled / not tracked.
2. Wait for the session to expire.
3. In tab A, do something that causes the SDK to renew the session, and this time the new session lands in the *tracked* bucket.
4. Switch to tab B (do **not** interact with it — don't click, don't navigate, just let background things like XHRs, long tasks, errors etc. happen).

Tab B keeps sending RUM events to the intake, and those are the ones showing up without a `sessionId`. Tab B never had a chance to react to the renewed session — from its point of view it's still on the last view of the now-expired session — yet events from it keep flowing through.

I'd expect the SDK to simply **not send** RUM events when it can't attach them to a real session. A tab that hasn't seen any actual user interaction since the session was renewed shouldn't be silently producing orphan events in the backend.
