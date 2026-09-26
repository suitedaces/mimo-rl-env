Keep track of ingest_took statistic in bulk operation type.
I'm currently writing a track that benchmarks an ingest processor and in order to see the impact of this ingest processor isolated from indexing itself, `ingest_took` field from bulk response should be examined.

Currently I check the service time (~~which I think is `took` field from bulk response~~), but that includes also the time it took the index the documents.
