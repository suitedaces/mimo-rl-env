## MDM command response with unknown command UUID returns 500

After migrating some hosts into Fleet's MDM (nanomdm), I'm seeing 500s on the MDM checkin endpoint when those hosts POST a command response.

The scenario: a host was previously managed by another MDM, gets enrolled into Fleet, and then phones home with a `CommandUUID` for a command we never queued on our side (it was queued by the previous server). When that response hits `/mdm`, Fleet returns a 500 to the device. The `mdmclient` on the device gets confused by that — it doesn't retry cleanly, and we lose the opportunity to send it any of the commands we *did* queue for it on the Fleet side.

From the host's perspective there's nothing wrong with the response — it's a perfectly valid Apple MDM payload, it just references a command UUID this server doesn't know about. A 500 feels wrong here; the device followed protocol, and on top of that the 500 prevents the normal "respond with the next queued command" flow from running, so the host stays stuck.

It would be much better if the server tolerated this case: accept the response (logging enough info that we can see it happened — command uuid, request type, status), and still hand the host its next queued command in the reply. Returning 500 should be reserved for actual server-side failures.

This is an edge case that I think only really shows up during migrations, but right now it's bad enough to block those hosts from receiving any further MDM commands until something else nudges them.
