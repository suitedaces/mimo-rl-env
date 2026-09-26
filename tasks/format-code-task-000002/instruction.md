on internal,

request:

```json
{
	"jsonrpc":"2.0",
	"method":"zkevm_batchNumberByBlockNumber",
	"params":[
		"87377"
	],
	"id":1
}
```

response:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32000,
        "message": "failed to get batch number from block number"
    }
}
```
