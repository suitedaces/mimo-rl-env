## Feature request: BYO SSL certificate support for `linode_object_storage_bucket`

I'm using Linode Object Storage to host a static site under a custom domain, and Linode lets me upload my own TLS certificate + private key for the bucket so it can be served over HTTPS at my domain. Today I can do this through the Cloud Manager UI (or by hitting the API directly), but the `linode_object_storage_bucket` resource in this provider doesn't expose anything for it — it only takes `cluster` and `label`.

That means my certificate ends up living outside Terraform. Every time I `terraform apply` I'm worried about drift, and when my cert is renewed I have to remember to go upload the new one out-of-band. It would be much nicer to keep everything declarative.

Could the `linode_object_storage_bucket` resource be extended so that I can attach a TLS certificate (the PEM-encoded cert + the corresponding private key) to the bucket directly from my Terraform config? Ideally:

- When I create a new bucket with a cert configured, the cert is uploaded as part of the apply.
- When I rotate / renew the cert (e.g. after Let's Encrypt issues a new one) and re-apply, the bucket's cert is updated to match.
- When I remove the cert from the config, the bucket goes back to having no custom cert.
- The cert material should be treated as sensitive so it isn't echoed in plan output.

Buckets that don't need HTTPS / custom certs should keep working exactly as before — this should be optional.

The new HCL surface I'd expect is something like a nested `cert { certificate = "...", private_key = "..." }` block on the resource.
