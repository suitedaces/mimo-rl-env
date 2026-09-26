## Feature request: query a service in a specific datacenter

I'm setting up diplomat in an org that runs Consul across multiple datacenters (e.g. `us-east-1` and `us-west-2`). From a Ruby app running in one DC I'd like to look up services that live in another DC.

Right now I'm doing something like:

```ruby
Diplomat::Service.get('my-service', :all)
```

which always returns whatever's registered in the local datacenter. Looking at `Diplomat::Service#get`, the only knobs on the `options` hash today are `wait` and `index` — there's no way to ask for a different DC.

Consul's HTTP catalog endpoint itself supports targeting a specific datacenter via a query parameter (see the [catalog docs](https://consul.io/docs/agent/http/catalog.html#catalog_service)), so it would be great if `Service#get` exposed that on the options hash too, in the same style as the existing `wait` / `index` entries. Then I could just pass the target datacenter alongside the service name and get back the nodes registered there.

Happy to add specs for it if useful.
