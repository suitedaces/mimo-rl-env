## `routeTableRanges` accepted by apiserver but causes Felix to panic

I'm trying out the `routeTableRanges` field on `FelixConfiguration` (the newer replacement for `RouteTableRange`). Since the docs say each entry can go up to `4294967295`, I tried something like:

```sh
calicoctl patch felixconfig default --type=merge -p \
  '{"spec":{"routeTableRanges": [{"Min": 1, "Max": 4294967295}]}}'
```

The patch is accepted by the apiserver without complaint and the resource is stored. But after that, Felix on my nodes immediately falls over and goes into a crash loop on startup — it never gets healthy again. I have to revert the FelixConfiguration to recover.

I also tried splitting it across several smaller ranges that, when added together, cover a similarly huge number of tables, and got the same outcome: apiserver happily accepts the spec, Felix dies.

Looking at the docs for this field, there is a sentence:

> *Note*, for performance reasons, the maximum total number of routing tables that Felix will accept is 65535 (or 2^16).

So Felix itself has an upper bound on the *total* number of tables across all the ranges combined. But that limit doesn't appear to be enforced anywhere on the apiserver side — you can submit a `routeTableRanges` spec that blows past it, and the only feedback you get is Felix crashing later, which is pretty hard to debug if you don't already know about the limit.

It would be much better if the apiserver rejected such a `FelixConfiguration` up front, the same way Felix would reject it, so that `kubectl patch` / `calicoctl patch` fails immediately with a clear validation error instead of silently accepting a config that breaks the cluster.
