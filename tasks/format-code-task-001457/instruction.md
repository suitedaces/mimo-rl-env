[FEAT] Make `secrets` parameter optional so we can use this action just to get the token.
**Is your feature request related to a problem? Please describe.**
The `secrets` parameter should not be mandatory. There is the option for `exportToken`, which is what I want to use to configure the Vault Terraform provider. However, with `secrets` being mandatory, it requires me to read a secret that I do not need. 

**Describe the solution you'd like**
The `secrets` parameter to not be mandatory, and allow us to use this action to simply get a Vault token to pass into other tooling.  

**Describe alternatives you've considered**
Honestly, none. Just grabbing a secret for the sake of using this action? I suppose I could create my own action that simply gets the token itself and posts to the login endpoint, but why not just use this one when it does the job?

**Additional context**
I am evaluating this action to use JWT with Github OIDC, as a potential replacement for internal automation around Vault access from CI. When configuring the Terraform Vault provider, you minimally need an endpoint, a token and, in our case, a namespace. I just want that sweet, sweet token. I don't wish to pass secrets into Terraform directly for example. It seems unnecessary to read a secret just to use this action to get a token.

Harbor pilot acceptance: update the shipped `dist/index.js` bundle as well as the source and action metadata, so the action works when GitHub runs it without a `secrets` input.
