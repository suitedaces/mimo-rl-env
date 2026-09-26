## After upgrading to 1.55, the `deckhouse` Service still has stale EndpointSlices and `cm/deckhouse` checks get stuck

After updating Deckhouse to 1.55 I noticed something odd on the `deckhouse` Service in `d8-system`:

```
$ kubectl -n d8-system get endpointslices -l kubernetes.io/service-name=deckhouse
NAME              ADDRESSTYPE   PORTS               AGE
deckhouse         IPv4          9650,9651,9652      5m
deckhouse-abcde   IPv4          9650,9651,9652      30m
```

There are **two** EndpointSlices for the same Service:

- `deckhouse` — the one Deckhouse itself manages now (this is the new behavior in 1.55, fine)
- `deckhouse-<hash>` — the old one the built-in endpointslice-controller generated from the Service's selector, left over from before the upgrade

As a result `cm/deckhouse` checks stay stuck and webhook traffic ends up hitting the wrong endpoint occasionally (the manually-managed slice points at the real deckhouse pod, the controller-managed one points at whatever the selector matches at the moment, and they disagree during rollout).

Looking at the release notes / changelog it seems the intent in 1.55 was that Deckhouse takes over endpoint management itself and the old controller-generated slice gets cleaned up on startup. From the outside it does not look like that cleanup actually happens — I waited a long while, restarted the deckhouse pod, the `deckhouse-<hash>` slice keeps coming back / never goes away. Deleting it by hand with `kubectl delete endpointslice` works for a few seconds, then a new `deckhouse-<random>` slice shows up again, presumably re-created by the endpointslice-controller because the Service still has its selector.

Expected: after upgrading, the `deckhouse` Service in `d8-system` should end up with exactly one EndpointSlice — the one Deckhouse manages itself — and the stale controller-generated slice(s) should be gone for good (not re-created on the next reconcile).
