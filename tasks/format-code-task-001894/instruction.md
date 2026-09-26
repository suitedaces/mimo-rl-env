Custom annotation for pinning ips (single and dual stack)
The loadbalancerip field is gonna be deprecated (see https://github.com/kubernetes/kubernetes/pull/107235)

That has two implications:
- we need to have an alternative way to pin to a specific ip (the suggested way is to implement custom annotations on the service, see https://github.com/kubernetes/enhancements/pull/1992)
- that will enable us to pin both v6 and v4 addresses to the service (currently, only one is possible)

So, this issue is about having a custom annotation handled by metallb, that declares the user's will to use a specific ip (or ips).
See also https://github.com/kubernetes/enhancements/pull/1992#issuecomment-1000113208 for reference.
