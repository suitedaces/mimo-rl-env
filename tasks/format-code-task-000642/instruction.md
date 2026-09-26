## `metadata` KMS reads the user passphrase secret too eagerly at init time

We're using ceph-csi RBD with at-rest encryption, KMS type `metadata`, and we point it at a per-tenant K8s Secret via `secretName` / `secretNamespace` in the StorageClass (the `userSecret` style of configuration, where `encryptionPassphrase` lives in a Kubernetes Secret in the tenant's namespace).

Two problems with how this currently behaves:

1. **KMS init fails hard if the user secret isn't reachable at that moment.**
   When the driver initializes the `metadata` KMS, it immediately goes to the K8s API to read the tenant's `encryptionPassphrase` secret. If that secret isn't there yet (e.g. the tenant namespace / secret is being provisioned around the same time as the workload, or the API server is briefly unreachable), the whole KMS initialization errors out and we can't proceed with the volume operation at all. The provider doesn't actually need the passphrase yet at init time — it only needs it later when a DEK has to be encrypted or decrypted — so failing this early feels too strict.

2. **Updates to the passphrase in the K8s Secret don't take effect.**
   Once the KMS is initialized, the passphrase value seems to be held onto by the driver. If we rotate / change `encryptionPassphrase` in the underlying K8s Secret afterwards, ceph-csi keeps using the old value until we restart the driver pods. That's not great operationally — we'd expect the driver to always pick up the current value of the configured Secret when it actually needs to encrypt/decrypt.

What we'd like is for the `metadata` KMS to defer reading the passphrase Secret until it actually needs it (i.e. at the point of encrypting/decrypting a DEK or fetching the secret for a volume), instead of doing it once during initialization and caching the result. That way, transient unavailability of the Secret at init time doesn't break things, and a later update to the Secret is picked up without a driver restart.

The same fallback path that's there today should still work — if `userSecret` (`secretName` / `secretNamespace`) isn't configured, fall back to `encryptionPassphrase` in the StorageClass secrets like before.
