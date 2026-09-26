Legacy !m query compatibilty for multi-key object classes
The `!m` query syntax when querying multi-key RPSL object classes is
unexpectedly changed between v4 and legacy versions.

Legacy versions expect the key values to be separated with either ` ` or `-`.
v4 expects the key values to be concatenated with no separator.

For example, when querying `route` objects:

```
$  echo -e '!!\n!v\n!mroute,41.78.188.0/22AS37271\n!q' | nc rr.ntt.net 43
A22
IRRd -- version 4.1.7
C
A346
route:          41.78.188.0/22
descr:          Workonline Communications (Pty) Ltd
origin:         AS37271
notify:         noc@workonline.co.za
mnt-by:         MAINT-AS37271
changed:        benmaddison@workonline.co.za 20101201  #15:59:08Z
source:         RADB
rpki-ov-state:  not_found # No ROAs found, or RPKI validation not enabled for source
C
$  echo -e '!!\n!v\n!mroute,41.78.188.0/22-AS37271\n!q' | nc whois.radb.net 43
A37
# IRRd -- version 3.0.8 [25Apr2014]
C
A233
route:      41.78.188.0/22
descr:      Workonline Communications (Pty) Ltd
origin:     AS37271
notify:     noc@workonline.co.za
mnt-by:     MAINT-AS37271
changed:    benmaddison@workonline.co.za 20101201  #15:59:08Z
source:     RADB
C
```

As a result, it is not possible to construct a query that is acceptable across versions.
