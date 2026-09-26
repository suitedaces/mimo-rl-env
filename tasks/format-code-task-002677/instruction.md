我想让 Chainlink 的 libp2p peerstore 不只是内存里的，节点重启后之前记住的 peers 地址、协议这些还能从主 PostgreSQL 里恢复出来。现在我没看到 networking 里有现成的方式能直接用节点已有的 DB 做这个，迁移最好也能顺手把需要的存储准备好。

Expected outcomes:
- Persistent peerstore API: `networking.NewPeerstore(ctx context.Context, db *sql.DB) (p2ppeerstore.Peerstore, error)` returns a libp2p peerstore backed by the supplied SQL database rather than process memory alone.
- Peer data survives reconstruction: after adding peer information such as addresses or supported protocols through the returned peerstore, constructing another peerstore with the same database can read that information back.
- Migration support: running the Chainlink database migrations prepares storage for the persistent peerstore by creating `p2p_peerstore` when needed.
- Peerstore table shape: the migration-created `p2p_peerstore` table has a `key` column with `TEXT PRIMARY KEY` semantics and a `data` column with `BYTEA NOT NULL` semantics, and creation is safe when the table already exists.

Implementation notes:
- The concrete storage adapter, helper structure, and validation location are implementation choices as long as callers can use the existing Chainlink database handle through the public networking API and observe persistent libp2p peerstore behavior.
- The migration may be organized consistently with the existing migration system; tests should validate the resulting database behavior and schema rather than private helper names or migration internals.
