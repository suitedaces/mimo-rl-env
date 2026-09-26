## `ALLOWED_HOSTS` is being expanded to parent domain — siblings that I didn't list can embed comments

I run remark42 for a network of sites that all share one parent domain. I want only some of the subdomains to be able to embed comments, so I set:

```
REMARK_URL=https://comments.example.com
ALLOWED_HOSTS=https://blog.example.com,https://docs.example.com
```

My expectation: only `blog.example.com` and `docs.example.com` are allowed to embed the remark42 widget. Anything else (e.g. `staging.example.com`, `random.example.com`) should be rejected.

What actually happens: every other subdomain under `example.com` is also accepted as an allowed embedding host, even though I never listed it. It looks like the entries I gave in `ALLOWED_HOSTS` are being collapsed up to the bare parent domain `example.com` somewhere along the way, and then any host under that parent passes the check.

For my use case this defeats the whole point of `ALLOWED_HOSTS` — it should be an exact list of hosts that may host comments, not a hint that gets widened to the registrable parent domain. Subdomain A and subdomain B of the same parent are completely different sites for me and I need to be able to allow one without implicitly allowing the other.

Could `ALLOWED_HOSTS` be treated as the literal set of hosts the admin configured, so that only the hostnames I explicitly list are accepted?
