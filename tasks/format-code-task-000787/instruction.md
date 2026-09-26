## Sharing documents between multiple `InMemoryDocumentStore` instances

I'm building a RAG setup with Haystack 2 where I have a separate indexing pipeline and a query pipeline. Both of them need to operate on the same set of documents, but right now every `InMemoryDocumentStore()` I create is a completely independent in-memory dict, so the query pipeline ends up seeing zero documents unless I explicitly pass the same Python object around.

A minimal repro of the surprise:

```python
from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore

store_a = InMemoryDocumentStore()
store_b = InMemoryDocumentStore()

store_a.write_documents([Document(content="Hello world")])

print(store_a.count_documents())  # 1
print(store_b.count_documents())  # 0
```

Other document stores (Chroma, Pinecone, Weaviate, …) let you point multiple client instances at the same logical collection by name, and the data is shared. With `InMemoryDocumentStore` there's no equivalent — the only way to share state today is to literally hand the same instance around, which is awkward when you build two pipelines in different places (e.g. one for indexing, one for querying), or when you want to use the default pipeline templates without pulling in `chroma-haystack` just to get shared storage.

It would be really useful if `InMemoryDocumentStore` supported some form of opt-in shared storage so that two instances created independently can refer to the same underlying documents. Default behavior should stay as it is now (each store is isolated) to avoid breaking anything; the sharing should be something the user explicitly asks for.

The new opt-in argument I'd expect is something like `index=...`, similar to how other vector DBs name their collection identifier.
