## Resource handshake error handler itself crashes when nonce sharing fails

I'm running a Golem node and occasionally a resource handshake with a peer
fails during the "share nonce" step — e.g. when hyperdrive upload of the
nonce file times out or the remote side is unreachable. I expect that to
fail cleanly: the peer's session should be notified and the handshake
should be marked as failed on our side.

What I'm actually seeing in the logs is different. The original hyperdrive
failure does get raised into the errback attached to `add_file(...)` in
`_share_handshake_nonce`, but instead of going through the normal
handshake-failure path, the errback itself blows up — it looks like
whatever it tries to call on the TaskServer side doesn't actually exist
there, so I get a second error on top of the first one and the real cause
gets buried. The peer's session never gets told that the handshake failed.

Repro is basically: trigger any failure inside the deferred returned by
`self.resource_manager.add_file(handshake.file, self.NONCE_TASK, ...)` in
`TaskResourcesMixin._share_handshake_nonce` (kill hyperdrive mid-upload,
or feed it a bad file). The errback fires and crashes immediately rather
than reporting the failure through the session that owns this handshake.

Could the errback in `_share_handshake_nonce` be fixed so that a failure
in nonce sharing is reported through the correct path and the session
for that peer gets notified, instead of the error handler crashing on
itself?
