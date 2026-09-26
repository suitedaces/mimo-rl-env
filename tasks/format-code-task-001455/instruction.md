Occasionally, when I mint a new TLS client cert to talk to my cluster infrastructure, the cert is rejected for a brief period of time. This turns out to be caused by a tiny amount of clock skew within my cluster, which made the server think the cert was only valid in the future. The skew was sub-second, my software and network was just fast enough to beat the clock :).

A common way to deal with this is to add a little slack to the NotBefore timestamp in the cert, e.g. put it 10-60s in the past (I've seen some folks suggest as much as 10 minutes). Vault should add such slack when issuing certificates.

It might also be worth calling out the importance of time synchronization (e.g. with NTP) in the TLS backend documentation. Combined with a small amount of slack, NTP sync should eliminate this class of mysterious failures (mysterious because most TLS stacks will just spit back "bad certificate", and people don't tend to question NotBefore).
