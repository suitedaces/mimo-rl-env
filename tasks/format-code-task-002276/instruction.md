## DM precheck rejects MySQL 8.0 source

I'm trying to set up a DM task with a MySQL 8.0 instance as the upstream. When DM runs the pre-check against the source, the MySQL version check fails and the task can't start — the error complains that my server's version is too high to be supported.

MySQL 8.0 has been GA for a while and is a pretty common upstream choice now, so it would be great if DM stopped flagging 8.0 servers as unsupported. As far as I can tell from running it, replication from 5.7 works fine, and there's no fundamental reason 8.0 shouldn't be allowed through the same checker.

Could the version checker be relaxed so MySQL 8.0 (and later) is accepted as a valid upstream?
