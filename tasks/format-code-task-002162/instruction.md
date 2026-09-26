## Feature request: expose metrics about which extra packages users install

I'm running an ASU instance and scraping its Prometheus metrics endpoint. Right now I can see total build counts (per branch/version/target/profile) and cache hit/miss numbers, which is useful, but there's one thing I'd really like to know that isn't exposed today: **which packages people are actually adding to their custom images**.

The use case is pretty concrete: when someone requests a build through ASU, they typically pick a profile and then tack on a bunch of extra packages on top of whatever that profile ships by default. As the operator of the instance I'd love to know what those "on top" packages are and how often each one gets requested — it would help me decide things like which packages to suggest more prominently, whether some popular community package should be considered for default inclusion, etc.

From the metrics side I currently get nothing on this. The builds counter tells me a build happened but says nothing about its package list, and obviously I don't want to just count every package in every manifest (that would be dominated by default packages that the user didn't actually choose). What I care about is specifically the *delta* over the profile's default package set.

Could ASU keep track of how many times each non-default package gets requested across builds, and surface that as a Prometheus metric (one sample per package name with the install count)? That way I can graph the top-N extra packages over time straight from Grafana.

Thanks!

(For what it's worth on the metric shape, I'd expect something along the lines of `extra_package_installs{package="..."}` so each non-default package becomes its own labelled sample.)
