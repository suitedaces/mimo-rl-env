A cluster instance can be created even with a different engine from cluster.
Cluster instance creation is not possible if engine is different from that of the cluster.

### example

```python
    target_cluster_identifier = "test-cluster"
    target_instance_identifier = "test-instance"
    rds_client = boto3.client("rds")
    rds_client.create_db_cluster(
        DBClusterIdentifier=target_cluster_identifier,
        Engine="aurora-postgresql",
        EngineVersion="12.14",
        MasterUsername="test-user",
        MasterUserPassword="password",
    )

    # Error should be raised here because of different engine versions.
    rds_client.create_db_instance(
        DBClusterIdentifier=target_cluster_identifier,
        Engine="mysql",
        EngineVersion="12.14",
        DBInstanceIdentifier=target_instance_identifier,
        DBInstanceClass="db.t4g.medium",
    )

```
