## qna-transformers `ask`: only the first result gets an answer, and there's no way to surface the best match

I'm using the `qna-transformers` module with GraphQL `ask`, something like:

```graphql
{
  Get {
    Article(
      ask: { question: "What is the capital of the Netherlands?", properties: ["content"] }
      limit: 10
    ) {
      title
      _additional {
        answer { result hasAnswer certainty property startPosition endPosition }
      }
    }
  }
}
```

Two things feel off about the behavior I'm getting:

1. **Only the first object in the result list gets an `answer` populated.** All the other objects come back with no `_additional.answer` at all (or `hasAnswer: false`). I'd expect the QnA extraction to run against each returned object's text properties, so any of them that actually contains the answer can be reported as such. Right now if the best-matching object happens to be #2 or #5 in the vector search result, I just don't see an answer for it.

2. **Even if every object did get an answer, the result order is still whatever the vector search returned.** The object that actually contains a high-certainty answer to my question isn't necessarily the one ranked first. For a Q&A use case I really want the top result to be the one most likely to actually answer the question, not just the closest vector. It would be great to have an option on the `ask` argument to reorder the results so the ones with the strongest answer come first; I'd want it opt-in so existing queries that rely on the original ordering aren't affected.

Both of these together make the qna feature awkward to use at `limit > 1` — you basically have to set `limit: 1` and hope the vector search already put the right object on top.

For the opt-in reordering option, I'd imagine calling it something like `rerank: true` on the `ask` argument.
