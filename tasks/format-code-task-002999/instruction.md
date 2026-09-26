## Inspect an OpenPGP key before importing it

In the account and key-import parts of the app we want to show users the details
of an OpenPGP key *before* they decide to import or trust it. Right now the crypto
layer can only tell us the fingerprint and key id of a key that has already been
imported — there is no way to look at an arbitrary armored key block and pull out
who it belongs to and how strong it is.

Add a capability to the PGP crypto API that, given an **armored OpenPGP key block**,
reads back the key's parameters for display.

Expose it as a synchronous method:

```
pgp.getKeyParams(armoredKey)
```

It must return a plain object with exactly these fields:

- `_id` — the key's 16-character hexadecimal key id, upper-cased.
- `fingerprint` — the key's 40-character hexadecimal fingerprint, upper-cased.
- `userId` — the email address of the key's primary identity.
- `userIds` — an array with one entry per identity on the key, in key order.
  Each entry is an object `{ name, emailAddress }` where `name` is the identity's
  display name and `emailAddress` is its email address, both with surrounding
  whitespace trimmed out of the underlying `Name <email>` identity string.
- `bitSize` — the key's bit length, as a number.

Behavioral details:

- It must accept both **public** and **private** armored key blocks, and produce
  the same parameters for the public and private halves of one key pair.
- When called **without** an armored key, it describes the key pair the instance
  currently holds (the one set by a successful import). If the instance has no key
  available in that case, it raises an `Error`.
- When given input that cannot be parsed as an OpenPGP key, it raises an `Error`.
