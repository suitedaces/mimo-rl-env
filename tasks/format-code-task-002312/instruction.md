# Make aggregate connection options self-contained initializers

The client options that configure aggregate connections — `aggregate`, `cluster` and
`replication` (the option classes under `Predis\Configuration\Option`) — should expose a single,
consistent contract: instead of just storing whatever the user supplied, each of these options must
**always return a callable "initializer"** that the client can invoke later to build a fully
configured `Predis\Connection\AggregateConnectionInterface` instance.

Rework these three options so they behave as described below.

## The initializer returned by the option

`filter()` (and, where a default exists, `getDefault()`) must return a callable. That callable is
the initializer and accepts two arguments:

```
$initializer($parameters, $autoaggregate = false)
```

* `$parameters` is the set of connection parameters (typically the list of nodes passed to the
  client).
* `$autoaggregate` is an optional boolean, defaulting to `false`.

When the initializer is invoked it must call the **user-supplied callable**, passing it exactly
three arguments, in this order:

1. the connection parameters,
2. the options container (`Predis\Configuration\OptionsInterface`),
3. the option instance itself (`Predis\Configuration\OptionInterface`).

The parameters must be handed to the user callable **by reference**, so a callable that declares its
first argument by reference can mutate them. The user callable must return an instance of
`Predis\Connection\AggregateConnectionInterface`; if it returns anything else, the initializer must
throw an `InvalidArgumentException`.

## Auto-aggregation

After the user callable returns a valid aggregate connection, the initializer decides whether to
populate it with the nodes found in `$parameters`:

* If `$autoaggregate` is `true` **and** `$parameters` is a non-empty list, every node in
  `$parameters` is added to the aggregate connection. A node that is already a
  `Predis\Connection\NodeConnectionInterface` is added as-is; anything else is first turned into a
  node connection using the options' connection factory (`$options->connections`).
* If `$autoaggregate` is `false` (or omitted), or if `$parameters` is empty, nothing is added.

Because the parameters are passed by reference, a user callable that empties them (e.g. sets them to
an empty array or `null`) disables auto-aggregation regardless of the `$autoaggregate` flag.

## Accepted values per option

**`aggregate`** accepts only a callable. Passing a non-callable value to `filter()` must throw an
`InvalidArgumentException`. It has no default initializer.

**`cluster`** accepts either a callable or one of the descriptive strings below; any other value
(e.g. a boolean, or an object that is not callable) must throw an `InvalidArgumentException`. Its
default initializer (and the `predis` string) builds a `Predis\Connection\Cluster\PredisCluster`.

* `predis` → `Predis\Connection\Cluster\PredisCluster`
* `redis` → `Predis\Connection\Cluster\RedisCluster`
* `redis-cluster` → `Predis\Connection\Cluster\RedisCluster`
* any other string → `InvalidArgumentException`

**`replication`** accepts either a callable or one of the descriptive strings below; any other value
must throw an `InvalidArgumentException`. Its default initializer (and the `predis` string) builds a
`Predis\Connection\Replication\MasterSlaveReplication`.

* `predis` → `Predis\Connection\Replication\MasterSlaveReplication`
* `sentinel` → `Predis\Connection\Replication\SentinelReplication`
* `redis-sentinel` → `Predis\Connection\Replication\SentinelReplication`
* any other string → `InvalidArgumentException`

The string-based and callable-based initializers must all obey the same wrapping contract described
above (argument order, return-type validation, and auto-aggregation behaviour).
