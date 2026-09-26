# Add chain awareness to shard identification

Right now a shard is identified by a 32-bit *branch value* that only encodes a
shard size and a shard id. We are moving to a multi-chain layout where every
shard also belongs to a chain, so the identifier needs to carry a chain id as
well.

## The encoding

Define a **full shard id** as a 32-bit integer split into two halves:

- the **high 16 bits** hold the `chain_id`;
- the **low 16 bits** hold `shard_size | shard_id`, where `shard_size` is a
  power of two whose single set bit is the most-significant set bit of those low
  16 bits, and `shard_id` is whatever remains below that bit.

So a full shard id is `(chain_id << 16) | shard_size | shard_id`.

Separately, a **full shard key** is also a 32-bit integer whose high 16 bits are
a `chain_id` and whose low 16 bits are an arbitrary shard key. The shard id for a
given shard size is obtained by masking the low key with `shard_size - 1`.

## What `Branch` must expose

`Branch` wraps a full shard id in its `value`. It should be able to report, all
derived purely from `value`:

- the chain id;
- the shard size (a power of two) — derived from the low 16 bits only, so a
  non-zero chain id never changes the reported shard size or shard id;
- the shard id;
- the full shard id (i.e. the value itself).

It must also answer whether a given full shard key belongs to this branch: this
is true only when the key's chain id equals the branch's chain id **and** the
key's shard id (low key masked by `shard_size - 1`) equals the branch's shard
id. A key in the right shard but the wrong chain does not belong to the branch.

## What `Address` must expose

An `Address` carries a `full_shard_key`. Given a shard size it should compute the
**full shard id** the address maps to: take the chain id from the high 16 bits of
the key, take the shard id from the low key masked by `shard_size - 1`, and
combine them as `(chain_id << 16) | shard_size | shard_id`. If the supplied shard
size is not a power of two this must raise `RuntimeError`.

Re-homing an address into a branch must also respect the chain: producing the
address "in" a branch keeps the recipient, adopts the branch's chain id, and
rewrites the low shard key so the address lands on the branch's shard id while
preserving the higher (above `shard_size`) bits of the original low key. The
resulting full shard key must belong to that branch.
