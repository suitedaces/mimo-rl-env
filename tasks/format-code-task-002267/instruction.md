### Bug Report

We're running a TiDB cluster where the TiDB and TiKV versions don't perfectly match (rolling upgrade in progress). During normal workload, tidb-server occasionally crashes with a panic coming from the batch RPC receive path in `store/tikv`.

From what we can tell, when TiKV returns a batched response whose command variant TiDB doesn't recognize (e.g. a newer TiKV introduced a response type that this TiDB build wasn't compiled against), the conversion of the batch response into the internal `tikvrpc.Response` doesn't handle that case, and something further down dereferences a nil and brings the whole tidb-server down.

This is pretty bad — a single unknown response payload from TiKV takes out the entire SQL node, instead of just failing that one request.

### Expected behavior

If TiKV sends back a batched response whose command type TiDB doesn't know how to translate, the affected SendRequest call should return an error to its caller. tidb-server should keep running and keep serving other queries. An unknown response from TiKV must not be able to panic the process.
