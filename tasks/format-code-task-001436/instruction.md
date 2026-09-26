## Allow unauthenticated access to `/metrics` for Prometheus scraping

I'm running Drone behind a private network and would like our internal Prometheus instance to scrape the `/metrics` endpoint exposed by drone-server.

Right now the endpoint always requires a valid session, so a request without credentials gets:

```
Invalid or missing prometheus token
```

(HTTP 401), and a request from a non-admin/non-machine user gets `Access denied` (HTTP 403). This means in order for Prometheus to scrape Drone we have to provision a machine user, mint a token, and configure that token into the Prometheus scrape job — which is overkill when both services already live on a trusted internal network.

It would be great if there was an opt-in way to let the metrics endpoint serve responses anonymously. The default should remain the current authenticated behaviour so existing deployments don't suddenly start exposing metrics publicly — operators who want anonymous scraping should have to deliberately turn it on via configuration.
