Out of memory crash when objects have a large length field unrelated to array size
While writing tests for [GraphBrainz](https://github.com/exogen/graphbrainz) I noticed that my latest test was consistently crashing AVA. Running the single test alone was enough to cause an OOM error, always in `concordance.serialize`, and the object I was snapshotting was not large by any means.

I narrowed it down to the `length` field on my objects. This field has nothing to do with array lengths, rather the meaning in this context is a recording length in milliseconds.

```js
[
  {
    title: "Airbag",
    length: 284400
  },
  {
    title: "Paranoid Android",
    length: 383493
  },
  // …more…
]
```

Concordance seems to be assigning some special meaning to these `length` fields and allocating memory based on them.

Try this and you'll notice it takes quite a long time and uses a lot of memory:

```
> concordance = require('concordance');
> concordance.serialize(concordance.describe({ length: 12345678 }));
```

It's possible this could be the cause of several of the OOM bug reports opened for AVA.

<details>
<summary>Stack trace</summary>

```
==== JS stack trace =========================================

    0: ExitFrame [pc: 0x3241121dc01d]
Security context: 0x3f5ee919e681 <JSObject>
    1: encode [0x3f5ecb13e4a1] [/Users/brianbeck/Projects/graphbrainz/node_modules/concordance/lib/encoder.js:~177] [pc=0x3241125889c2](this=0x3f5ecfec66f9 <Object map = 0x3f5eefa91039>,serializerVersion=2,rootRecord=0x3f5ecb13e771 <Object map = 0x3f5eefa94319>,usedPlugins=0x3f5ecb145bf9 <Map map = 0x3f5e362045c1>)
    2: serialize [0x3f5ecb102e21] [/Users/b...

FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory
 1: 0x100039dbf node::Abort() [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 2: 0x100039fc9 node::OnFatalError(char const*, char const*) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 3: 0x1001d1375 v8::internal::V8::FatalProcessOutOfMemory(v8::internal::Isolate*, char const*, bool) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 4: 0x10059c572 v8::internal::Heap::FatalProcessOutOfMemory(char const*) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 5: 0x10059f045 v8::internal::Heap::CheckIneffectiveMarkCompact(unsigned long, double) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 6: 0x10059aeef v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 7: 0x1005990c4 v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 8: 0x1005995c5 v8::internal::Heap::CollectAllAvailableGarbage(v8::internal::GarbageCollectionReason) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
 9: 0x1005a5a21 v8::internal::Heap::AllocateRawWithRetryOrFail(int, v8::internal::AllocationSpace, v8::internal::AllocationAlignment) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
10: 0x100574da6 v8::internal::Factory::NewFixedArrayWithFiller(v8::internal::Heap::RootListIndex, int, v8::internal::Object*, v8::internal::PretenureFlag) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
11: 0x10051c2de v8::internal::(anonymous namespace)::ElementsAccessorBase<v8::internal::(anonymous namespace)::FastPackedObjectElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)2> >::GrowCapacity(v8::internal::Handle<v8::internal::JSObject>, unsigned int) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
12: 0x1007b6f9f v8::internal::Runtime_GrowArrayElements(int, v8::internal::Object**, v8::internal::Isolate*) [/Users/brianbeck/.nvm/versions/node/v10.10.0/bin/node]
13: 0x3241121dc01d
Abort trap: 6
```

</details>
