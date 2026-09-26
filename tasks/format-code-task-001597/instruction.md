### JWT authentication policy with an HTTPS issuer doesn't work

I'm trying to set up end-user (origin) JWT authentication on 0.8 using an `authentication.Policy` that points at a real public OIDC provider (in my case Google, but I'd expect the same for Auth0/Okta/etc.). Something like:

```yaml
apiVersion: authentication.istio.io/v1alpha1
kind: Policy
metadata:
  name: jwt-example
spec:
  targets:
  - name: my-svc
  origins:
  - jwt:
      issuer: "https://accounts.google.com"
  principalBinding: USE_ORIGIN
```

I'm intentionally not setting `jwks_uri` — I want pilot to discover it via the standard `/.well-known/openid-configuration` endpoint.

After applying the policy, JWT auth doesn't take effect on the sidecar. In pilot's logs I see it failing to resolve the `jwks_uri` for the issuer; the configured policy never actually gets a usable public key wired in, so requests aren't validated against the JWT as I'd expect.

If I host the same OIDC metadata + JWKS on a plain HTTP server inside the cluster and point `issuer` / `jwks_uri` at that, things work. The problem only shows up when pilot has to talk to a real HTTPS OIDC provider on the public internet.

This pretty much blocks using JWT origin authentication with any standard external identity provider, since they're all HTTPS-only. Pilot needs to be able to reach an HTTPS issuer to pull the OpenID discovery doc and the JWKS.
