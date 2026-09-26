## Add support for `proof_of_possession` on resource servers

I'm using auth0-deploy-cli to manage my tenant configuration as code. One of my APIs needs proof-of-possession (DPoP) enabled on the access tokens it issues — Auth0's Management API exposes a `proof_of_possession` setting on resource servers for exactly this.

When I add `proof_of_possession` to the resource server entry in my YAML config and run an import, the deploy CLI doesn't recognize the field — the resource server schema only covers things like `enforce_policies`, `token_dialect`, scopes, etc.

Could the resource server schema be extended so that `proof_of_possession` is a recognized, validated field? I'd like to manage this setting through the CLI alongside the other resource server properties instead of having to configure it out-of-band.
