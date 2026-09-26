# Load payment orders when an identity unlocks

The payment order status tracker (in the `pilvytis` package) currently only learns about an
identity's orders by polling the pilvytis backend on a fixed interval. That means right after a
wallet/identity is unlocked there's a window where the node knows nothing about that identity's
existing orders until the next poll happens, and an order that was already completed while the node
was offline is noticed late (or its completion event is missed entirely).

I'd like the tracker to react to identity unlock events instead of relying purely on the timer.

## What I want

When an identity is unlocked, the tracker should immediately fetch that identity's orders from the
backend and bring its view of them up to date, publishing the usual order-updated notifications so
the rest of the node (balance resync, etc.) can react.

Concretely:

- The tracker should be able to register itself on an event bus. Follow the same
  `Subscribe(bus eventbus.Subscriber) error` convention used by the other components in this
  codebase. Once subscribed, it must react to the identity-unlock event that the identity manager
  publishes (topic `identity.AppTopicIdentityUnlock`, payload `identity.AppEventIdentityUnlock`).

- Reacting to an unlock means: load all of that identity's orders from the backend and reconcile
  them with what the tracker already knew, emitting an `AppEventOrderUpdated` (on the tracker's
  event bus, topic `AppTopicOrderUpdated`) in exactly these situations:
    - An order that was already being tracked has changed status — emit one event reflecting the
      new state.
    - An order that has never been seen before for that identity is already in a **final** state
      (anything other than the in-progress statuses `new`, `pending`, `confirming`) — emit one
      event for it, because we may have missed its completion.
  A previously unseen order that is still **in progress** (`new`/`pending`/`confirming`) must be
  recorded silently — no event — and only produce an event later, once its status actually changes.

- Reconciliation must be idempotent and per-identity:
    - Loading the same orders again with no changes must not re-publish anything.
    - Orders are tracked separately per identity; the same numeric order id belonging to two
      different identities are independent, and unlocking one identity must only load that
      identity's orders.

The node already tracks order statuses by periodically polling, and that existing behavior together
with its current public surface must keep working unchanged — this is an addition on top of it, not
a replacement.
