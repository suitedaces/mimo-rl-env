## Feature request: parse and expose room access / join / history visibility state

I'm writing a client on top of nio and I want to surface a few basic things about each joined room in my UI:

- Whether guests are allowed in the room (`m.room.guest_access`)
- The room's join rule, e.g. whether it's invite-only or public (`m.room.join_rules`)
- The room's history visibility, e.g. whether new members can read older messages or the room is world-readable (`m.room.history_visibility`)

These are all standard state events from the client-server spec:

- https://matrix.org/docs/spec/client_server/latest.html#m-room-guest-access
- https://matrix.org/docs/spec/client_server/latest.html#m-room-join-rules
- https://matrix.org/docs/spec/client_server/latest.html#m-room-history-visibility

Right now after a sync I have a `MatrixRoom` instance and there's no way to read any of these — the room object exposes `name`, `topic`, `canonical_alias`, `creator`, `federate`, `room_version`, `encrypted`, etc., but nothing for guest access / join rule / history visibility. Looking at `parse_event` these three event types also aren't recognized, so they end up as `UnknownEvent` and are never reflected on the room.

It would be great if nio handled these the same way it already handles `m.room.create` / `m.room.name` / `m.room.topic`: parse them into proper event types and update the corresponding state on `MatrixRoom` when `handle_event` sees them, so that consumers can just read the current value off the room object after a sync.
