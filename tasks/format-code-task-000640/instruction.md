### Allow per-client ping/pong configuration

Right now the application-level ping/pong settings (ping interval and pong timeout) can only be configured at the transport / handler level — every client served by the same handler ends up with identical ping behavior.

In our setup we'd like to vary this per connection. For example:

- Mobile clients on flaky networks: we want a more aggressive ping interval to detect dead connections faster.
- Long-lived desktop clients on stable networks: we'd prefer a much longer ping interval to save bandwidth/battery on the server side.

We have all the information needed to make that decision inside `OnConnecting` (we look at the token claims / client name / version), so it would be very natural to make the decision there and return it as part of the `ConnectReply`. Today there is no way to do that — once the client is created it just picks up whatever the transport reports, and we'd have to register a separate handler/endpoint per client class just to get a different ping interval, which is awkward.

Would it be possible to let `OnConnecting` optionally override the ping/pong settings for the connection being established? If nothing is returned, the existing transport-level default should still apply, so existing code keeps working.

One small side note while you're in that area: the transport interface currently exposes this as `AppLevelPing()` returning an `AppLevelPing` struct, while the handler configs already embed a `PingPongConfig` for the same concept. Having two names for the same thing is a bit confusing when reading the code — it would be nice if these were unified.
