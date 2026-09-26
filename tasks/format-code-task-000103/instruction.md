## `FetchServiceImageMetaData` on `ConfigAgent` is a pure passthrough — remove it and call dbdaemon directly

Looking at how `isImageSeeded` (in the instance controller) gets the service image metadata today, it goes through `ConfigAgent`:

```
isImageSeeded
  -> ConfigAgent client.FetchServiceImageMetaData
       -> dbdaemon client.FetchServiceImageMetaData   // actually does the work
```

But if you check the `ConfigAgent` server implementation of `FetchServiceImageMetaData`, it doesn't do anything meaningful: it just dials dbdaemon, forwards the request, and repacks the response field-for-field into the equivalent `ConfigAgent` proto. No additional logic, no enrichment, no decision-making — purely a wrapper.

This forces us to maintain a redundant set of `FetchServiceImageMetaDataRequest` / `FetchServiceImageMetaDataResponse` messages on the `ConfigAgent` proto that mirror the dbdaemon ones one-to-one, plus an extra network hop and an extra RPC surface to keep in sync. The `ConfigAgent` is supposed to host orchestration / business logic that sits above raw dbdaemon calls; a thin forwarder like this doesn't belong there.

`isImageSeeded` is currently the only caller of the `ConfigAgent` version, and the instance controller already has a `DatabaseClientFactory` available for talking to dbdaemon directly. So the `ConfigAgent` layer here isn't even buying us a stable abstraction for multiple callers — it's dead weight on a single call site.

I'd like to remove `FetchServiceImageMetaData` from the `ConfigAgent` surface entirely and have `isImageSeeded` talk to dbdaemon directly via the database client. The behavior observed by the controller should be identical (same metadata, same `SeededImage` interpretation), it's just one less hop and one less proto pair to maintain.
