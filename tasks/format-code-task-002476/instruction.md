# Reusable Matrix user/address reachability helper

Our Matrix transport currently buries all of its "is this peer node online?" bookkeeping inside the
transport object. Other services (e.g. the pathfinding service) now need the same capability —
mapping Matrix users to Ethereum node addresses and deriving whether a node is reachable from the
Matrix presence updates — but they don't run a full transport. Please extract this into a
standalone, reusable helper that lives in the Matrix transport package and can be driven by any
Matrix client.

## What to build

A helper class — importable from the Matrix transport package as `UserAddressManager` — that tracks
the many-to-one mapping of Matrix users to Ethereum addresses and synthesizes a per-address
*reachability* state from the per-user *presence* state. A single Ethereum node may be controlled by
several Matrix users (one per homeserver), so reachability must be composed across all users known
for an address.

Alongside it, expose two enums from the same package:

- `UserPresence`, with members `ONLINE` (`'online'`), `UNAVAILABLE` (`'unavailable'`),
  `OFFLINE` (`'offline'`) and `UNKNOWN` (`'unknown'`) — the member values are the strings used in
  Matrix presence events.
- `AddressReachability`, with members `REACHABLE`, `UNREACHABLE` and `UNKNOWN`.

### Construction

`UserAddressManager` is created with:

- `client`: a Matrix client object.
- `get_user_callable`: a callable taking a user id (or user object) and returning a user object that
  exposes `.user_id` and `.displayname`.
- `address_reachability_changed_callback`: called as `(address, reachability)` whenever an address's
  synthesized reachability *changes*.
- `user_presence_changed_callback` (optional): called as `(user, presence)` whenever a user's
  presence *changes*.
- `stop_event` (optional): a `gevent` event; when set, incoming presence updates are ignored.

On construction the manager must register itself as a presence listener on the given client (via the
client's `add_presence_listener`), so that presence events delivered by the client drive its state.

### Tracked addresses

The manager only reacts to presence for addresses that have been explicitly registered as
interesting. Provide:

- `add_address(address)` — start tracking an address.
- `add_userid_for_address(address, user_id)` and `add_userids_for_address(address, user_ids)` — add
  one or many user ids for an address; either implicitly starts tracking the address if it was not
  known yet.
- `is_address_known(address) -> bool`.
- `known_addresses` — the collection of all tracked addresses.
- `get_userids_for_address(address)` — the set of user ids known for the address (empty set for an
  unknown address).
- `get_userid_presence(user_id) -> UserPresence` — the last known presence for a user, or
  `UserPresence.UNKNOWN` if none is known.
- `get_address_reachability(address) -> AddressReachability` — the current synthesized reachability,
  or `AddressReachability.UNKNOWN` if unknown.

### Presence handling and reachability synthesis

When the client delivers a presence event, the manager must ignore it if any of the following hold:
the stop event is set; the event is not a Matrix presence event (`type` other than `'m.presence'`);
the event is about the client's own user; the sender's user id does not validate to an Ethereum
address; or the resolved address is not currently tracked. Otherwise it records the user under that
address, updates the cached per-user presence, and re-synthesizes the address reachability.

An individual user's presence maps to reachability as: `ONLINE` and `UNAVAILABLE` →
`REACHABLE` (an "unavailable" user is merely idle, but still reachable); `OFFLINE` → `UNREACHABLE`;
`UNKNOWN` → `UNKNOWN`. For an address with several users, the synthesized presence is the
"most available" presence among them, using the ordering `ONLINE` > `UNAVAILABLE` > `OFFLINE` >
`UNKNOWN` (i.e. a single online user makes the address reachable regardless of the others); the
address reachability is then derived from that synthesized presence. An address with no associated
user presence is `UNKNOWN`.

Callbacks fire only on transitions: the reachability callback must be invoked only when an address's
reachability actually changes, and the user-presence callback only when a user's presence actually
changes. Re-receiving the same presence for a user must not invoke either callback.

### Additional control methods

- `refresh_address_presence(address)` — recompute an address's reachability from the currently cached
  user presences and fire the reachability callback if it changed. For any user whose presence is not
  yet cached, fall back to querying the client (`get_user_presence`), treating a failed lookup as
  `UNKNOWN`. This must not invoke the user-presence callback.
- `force_user_presence(user, presence)` — directly set the cached presence for a user without
  recomputing reachability and without firing any callback. (Used to paper over a Matrix protocol
  edge case; a subsequent `refresh_address_presence` is what actually applies it.)

Make sure the existing Matrix transport keeps working with these enums (it already relies on a
`UserPresence` enum with the same members and values).
