## NPE when setting `dynamic_partition.buckets` on a non-partitioned table

I have a regular (non-partitioned) OLAP table and I wanted to tweak the bucket count via a dynamic partition property. When I run something like:

```sql
CREATE TABLE t (
    k1 INT,
    v1 INT
) DISTRIBUTED BY HASH(k1) BUCKETS 8
PROPERTIES (
    "dynamic_partition.buckets" = "10"
);
```

(or the equivalent `ALTER TABLE ... SET ("dynamic_partition.buckets" = "10")` on an existing non-partitioned table)

the FE crashes with a NullPointerException instead of giving me a useful error.

If I instead pass any of the other dynamic partition properties (e.g. `dynamic_partition.enable`, `dynamic_partition.time_unit`, `dynamic_partition.end`, ...) on the same non-partitioned table, I get a clean, readable error telling me that dynamic partition is only supported on single-column range-partitioned tables. That's the behavior I'd expect here too — `dynamic_partition.buckets` shouldn't be treated as a special case that bypasses validation and blows up later with an NPE.

Either reject it up front with the same kind of error message as the other `dynamic_partition.*` properties, or otherwise handle it gracefully. Just please don't NPE.
