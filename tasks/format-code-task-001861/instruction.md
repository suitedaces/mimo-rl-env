[MSC2414](https://github.com/matrix-org/matrix-doc/pull/2414) made the `reason` and `score` parameters for the [POST /_matrix/client/r0/rooms/{roomId}/report/{eventId}](https://matrix.org/docs/spec/client_server/r0.6.1#post-matrix-client-r0-rooms-roomid-report-eventid) endpoint.

That endpoint is implemented in Synapse here:

https://github.com/matrix-org/synapse/blob/8a4a4186ded34bab1ffb4ee1cebcb476890da207/synapse/rest/client/v2_alpha/report_event.py#L31-L46

The [Event Reports Admin API](https://github.com/matrix-org/synapse/blob/develop/docs/admin_api/event_reports.rst) should also be updated to state that the `reason` and `content` fields may be both blank and `null`, and the Admin API endpoint should be updated to expect `None` values for these keys as well:

https://github.com/matrix-org/synapse/blob/cbabb312e0b59090e5a8cf9e7e016a8618e62867/synapse/storage/databases/main/room.py#L1388-L1389

(that function may not actually need updating, but it would be good to check that the API still behaves as expected).

Some tests for clients sending reports without `reason` and `score` would be great as well.

This will need to be implemented in order to eventually advertise support for the next Client-Server API version.
