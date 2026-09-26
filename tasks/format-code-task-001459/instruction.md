When using the following hz xml only on retrieving the cache, I get a validation error. But the XML file could be validated when loaded. 

```xml
<hazelcast xsi:schemaLocation="http://www.hazelcast.com/schema/config
                               http://www.hazelcast.com/schema/config/hazelcast-config-3.8.xsd"
           xmlns="http://www.hazelcast.com/schema/config"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <group>
        <name>workers</name>
    </group>

    <lite-member enabled="true"/>

    <network>
        <port port-count="200" auto-increment="true">5701</port>
        <join>
            <multicast enabled="false"/>
            <tcp-ip enabled="true">
                <member>192.168.0.1:5701</member>
                <member>192.168.0.2:5701</member>
            </tcp-ip>
        </join>

         <ssl enabled="false"/>
    </network>

    <properties>
        <property name="hazelcast.phone.home.enabled">false</property>
    </properties>

    <license-key>...</license-key>

    <!--MANAGEMENT_CENTER_CONFIG-->

    <native-memory allocator-type="POOLED" enabled="true">
        <size unit="GIGABYTES" value="2" />
        <metadata-space-percentage>20</metadata-space-percentage>
    </native-memory>

    <cache name="cache">
        <eviction size="10000000" max-size-policy="ENTRY_COUNT" eviction-policy="LFU"/>
        <backup-count>1</backup-count>
        <async-backup-count>0</async-backup-count>
        <in-memory-format>NATIVE</in-memory-format>
    </cache>

</hazelcast>
```

```java
ERROR 2017-06-07 19:28:12,284 [Thread-5] com.hazelcast.simulator.worker.testcontainer.TestManager: --------------------------- global prepare of LongStringCacheTest FAILED --------------------------- 
java.lang.IllegalArgumentException: Invalid max-size policy (ENTRY_COUNT) for com.hazelcast.cache.hidensity.impl.nativememory.HiDensityNativeMemoryCacheRecordStore! Only USED_NATIVE_MEMORY_SIZE, USED_NATIVE_MEMORY_PERCENTAGE, FREE_NATIVE_MEMORY_SIZE, FREE_NATIVE_MEMORY_PERCENTAGE are supported.
	at com.hazelcast.cache.hidensity.impl.nativememory.HiDensityNativeMemoryCacheRecordStore.createCacheEvictionChecker(HiDensityNativeMemoryCacheRecordStore.java:121)
	at com.hazelcast.cache.impl.AbstractCacheRecordStore.<init>(AbstractCacheRecordStore.java:150)
	at com.hazelcast.cache.hidensity.impl.nativememory.HiDensityNativeMemoryCacheRecordStore.<init>(HiDensityNativeMemoryCacheRecordStore.java:59)
	at com.hazelcast.cache.EnterpriseCacheService.newNativeRecordStore(EnterpriseCacheService.java:243)
	at com.hazelcast.cache.EnterpriseCacheService.createNewRecordStore(EnterpriseCacheService.java:217)
	at com.hazelcast.cache.impl.CachePartitionSegment.createNew(CachePartitionSegment.java:51)
	at com.hazelcast.cache.impl.CachePartitionSegment.createNew(CachePartitionSegment.java:37)
	at com.hazelcast.util.ConcurrencyUtil.getOrPutSynchronized(ConcurrencyUtil.java:73)
	at com.hazelcast.cache.impl.CachePartitionSegment.getOrCreateRecordStore(CachePartitionSegment.java:67)
	at com.hazelcast.cache.impl.AbstractCacheService.getOrCreateRecordStore(AbstractCacheService.java:278)
```

It would be helpful if the shared cache-config validation logic were exposed as a reusable check (e.g. something like a `checkCacheConfig` helper on the internal config validator) so both XML loading and programmatic cache creation paths can invoke the same fail-fast validation.
