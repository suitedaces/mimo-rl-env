## Battery status from FindMy advertisements is not exposed

When I receive a FindMy advertisement and run it through `ParseData` in
`lib/findmy`, I get back the status byte, but there's no way in this
library to interpret what that byte means. Looking at what's available,
there's only a single `DefaultStatus` constant — everything else I see
in real advertisements (different values depending on whether the tag's
battery is full, getting low, almost dead, etc.) is just an opaque byte
to me.

Apple's FindMy protocol encodes the battery level into that status byte,
so a tag broadcasting "battery critical" looks different from one
broadcasting "battery full". Right now I'd have to hardcode the magic
numbers in my own app to figure out which is which, and every consumer
of this library would end up duplicating the same table.

It would be great if `lib/findmy` exposed the battery levels as part of
its public API so I can tell, from a parsed advertisement, roughly how
much battery a tag has left. Same goes for the other direction —
`NewData` currently stamps `DefaultStatus` into outgoing advertisements,
and it'd be nice if the meaning of that default were clearer (a freshly
provisioned tag should presumably advertise as having a healthy battery,
not just some unnamed default).

I'd expect something like exported `StatusBatteryFull` / `StatusBatteryMedium` / `StatusBatteryLow` / `StatusBatteryCritical` constants, plus a `BatteryStatus(b byte) string` helper that returns names like `"full"` / `"medium"` / `"low"` / `"critical"` (and `"unknown"` for unrecognized values).
