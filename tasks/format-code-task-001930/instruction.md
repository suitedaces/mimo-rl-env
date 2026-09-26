### Expected Behavior
Minio server should start successfully when its data directory lives on an EFS / NFS mount that has plenty of free space.

### Actual Behavior
When pointing minio at a directory backed by EFS (or some NFS exports), the server refuses to come up and reports the disk as full / unusable, even though `df -h` on the same mount shows lots of free space and the mount is otherwise healthy. The same minio binary, pointed at a local ext4 / xfs directory of similar size, starts up fine.

### Steps to Reproduce
1. Mount an EFS volume (or an NFS share whose server doesn't report a meaningful inode count) somewhere like `/mnt/efs/minio`.
2. `df -h /mnt/efs/minio` — shows e.g. hundreds of GB free.
3. `minio server /mnt/efs/minio`
4. Server fails to start with a disk-full style error.

### Context
EFS and several other network filesystems don't expose inode counts the way a local Linux filesystem does — the numbers they return over `statfs` are either zero, bogus, or essentially unbounded and don't reflect "how many files you can still create". Treating these values as a hard precondition for starting up makes minio unusable on those backends, which is a pretty common deployment target (AWS EFS, managed NFS, etc.).

Reference: #4675

Separately while looking at the storage info code path: the totals/free bytes are tracked as `int64`. On large aggregated deployments (many disks × multi-TB each) the multiplication done when reporting cluster-wide capacity can go negative — those quantities are inherently non-negative sizes and probably shouldn't be signed.
