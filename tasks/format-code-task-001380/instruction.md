## groups.Update for security groups doesn't seem usable

I'm trying to update an existing security group (just renaming it and tweaking the description) via the `openstack/networking/v2/extensions/security/groups` package, and I can't get `Update` to do anything useful.

The signature I see is:

```go
func Update(c *gophercloud.ServiceClient, opts UpdateOptsBuilder) (r UpdateResult)
```

I don't understand how this is supposed to know *which* security group I want to modify. `UpdateOpts` only carries `Name` and `Description` — no ID — and the function itself doesn't take one either. When I call it against my Neutron endpoint anyway, like:

```go
opts := groups.UpdateOpts{
    Name:        "new-name",
    Description: "renamed by automation",
}
res := groups.Update(client, opts)
if res.Err != nil {
    log.Fatal(res.Err)
}
```

…it just errors out, and nothing on the server side changes. Meanwhile `groups.Get(client, id)` and `groups.Delete(client, id)` against the same security group work fine, and `Create` works fine too — it's only `Update` that's broken for me.

Could `Update` be made to actually work like the other single-resource operations in this package? It looks like it's currently impossible to update a specific security group through this API at all.
