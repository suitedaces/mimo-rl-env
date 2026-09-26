## `kudo init` says cert-manager isn't installed, but it is

I'm trying to install KUDO on a cluster that already has a supported
version of cert-manager (0.10.1, per the KUDO docs) running, but
`kudo init` keeps failing the prereq check:

```
$ kubectl kudo init
$KUDO_HOME has been configured at /home/me/.kudo
✗ failed to detect any valid cert-manager CRDs. Make sure cert-manager is installed.
Error: prerequisites not installed : Yet
```

cert-manager is actually there and healthy though:

```
$ kubectl get pods -n cert-manager
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-xxxxxxxxxx-xxxxx              1/1     Running   0          3h
cert-manager-cainjector-xxxxxxxxxx-xxxxx   1/1     Running   0          3h
cert-manager-webhook-xxxxxxxxxx-xxxxx      1/1     Running   0          3h

$ kubectl get crd | grep cert-manager
certificates.cert-manager.io           2020-xx-xxT...
certificaterequests.cert-manager.io    2020-xx-xxT...
issuers.cert-manager.io                2020-xx-xxT...
clusterissuers.cert-manager.io         2020-xx-xxT...
challenges.acme.cert-manager.io        2020-xx-xxT...
orders.acme.cert-manager.io            2020-xx-xxT...
```

So from a user perspective cert-manager is clearly installed and the
CRDs are there. I can create `Issuer` / `Certificate` resources by hand
against this cluster and they work fine.

As a workaround I can pass `--unsafe-self-signed-webhook-ca` to skip
the cert-manager check entirely, but that defeats the point of having
cert-manager installed in the first place. `kudo init` should
recognize the existing cert-manager install and continue with the rest
of the setup.

Cluster is on the older side (the kind of setup where cert-manager
0.10.x is still the recommended version), if that's relevant.
