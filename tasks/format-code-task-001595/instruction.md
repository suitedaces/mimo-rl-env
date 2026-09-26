### Bug: revision tag created against an older control plane never gets a CA bundle, so injection fails

I'm trying to use `istioctl x revision tag` to put a stable alias in front of an older Istio control plane (we're running 1.9.x in this cluster and migrating gradually). Something like:

```
istioctl x revision tag set prod --revision 1-9-5
```

`istioctl` first warns me that the revision is older than 1.10 and asks "Continue anyways? (y/N)". I answer `y` because I genuinely want a tag pointing at this older CP. The command finishes and a `MutatingWebhookConfiguration` for the tag does get created.

The problem shows up as soon as I try to actually use the tag:

```
kubectl label ns test-ns istio.io/rev=prod
kubectl -n test-ns run nginx --image=nginx
```

The pod comes up with no sidecar. When I look at the tag's `MutatingWebhookConfiguration`, the `clientConfig.caBundle` field is empty. The webhook for the underlying `1-9-5` revision has a populated `caBundle` just fine — only the tag webhook is missing it, so the API server can't establish TLS to the injector and injection silently doesn't happen.

If I do the same thing against a 1.10+ revision it works, presumably because the newer istiod fills the bundle in after the fact. But the whole point of revision tags for us is to be able to point them at whichever revision we currently have running, including older ones during an upgrade. Having to upgrade the control plane *first* before tags become usable defeats the purpose.

### What I'd expect

`istioctl x revision tag set` should produce a tag webhook that actually works regardless of the target revision's istiod version, including revisions older than 1.10. I shouldn't have to manually go patch the `caBundle` on the generated webhook to make namespace injection start working.

### Version
istioctl: 1.10-dev (master)
control plane: 1.9.5
