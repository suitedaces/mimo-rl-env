### Custom notify / sessions endpoints set via environment variables are ignored

I'm running bugsnag-go against our self-hosted (on-premise) Bugsnag deployment and configuring everything through environment variables (we don't want internal URLs baked into the Go binary). My env looks like:

```
BUGSNAG_API_KEY=...
BUGSNAG_NOTIFY_ENDPOINT=https://errors.bugsnag.internal.example
BUGSNAG_SESSIONS_ENDPOINT=https://sessions.bugsnag.internal.example
```

and in code I just do:

```go
bugsnag.Configure(bugsnag.Configuration{
    ReleaseStage: "production",
    AppVersion:   buildVersion,
    // intentionally NOT setting Endpoints in code -
    // I want them to come from the env vars above
})
```

I'd expect error reports and session data to be POSTed to my internal hosts. Instead, nothing shows up on our internal Bugsnag dashboard. When I look at outbound traffic from the app, the notifier is actually calling the public SaaS endpoints (`notify.bugsnag.com` / `sessions.bugsnag.com`) — my env-var values appear to have no effect at all.

As a workaround, if I read the env vars myself and stuff them onto the `Endpoints` field of `Configuration`:

```go
bugsnag.Configure(bugsnag.Configuration{
    Endpoints: bugsnag.Endpoints{
        Notify:   os.Getenv("BUGSNAG_NOTIFY_ENDPOINT"),
        Sessions: os.Getenv("BUGSNAG_SESSIONS_ENDPOINT"),
    },
    ReleaseStage: "production",
    AppVersion:   buildVersion,
})
```

then everything works correctly — events arrive at the right place. So configuring via the `Configuration` struct directly is fine; it's specifically the "endpoints configured *only* through environment variables" path that doesn't take effect.

Since `BUGSNAG_NOTIFY_ENDPOINT` / `BUGSNAG_SESSIONS_ENDPOINT` are documented as a supported configuration channel, I'd expect setting them in the env to behave the same as setting `Endpoints` in code — including in the common case where the app only calls `Configure` with non-endpoint options (release stage, app version, etc.) and leaves the `Endpoints` field zero-valued.
