Federated RAG retrieval currently flattens module outputs, which makes it impossible to combine ranked evidence deliberately or report partial retrieval failures. Extend the public RetrievalRagStage and RagContext APIs with deterministic fusion and diagnostics while preserving concatenation as the default behavior.

RetrievalRagStage must accept these keyword options:

- `fusion_mode: Literal["concatenate", "rrf"] = "concatenate"`
- `rrf_k: float = 60`
- `module_weights: dict[str, float]`, defaulting to an empty mapping
- `on_error: Literal["raise", "continue"] = "raise"`

RagContext must expose serializable `retrieval_scores: dict[str, float]` and `retrieval_errors: dict[str, str]` fields, both empty by default. Each successful stage run replaces both diagnostics rather than retaining entries from a previous run.

For both fusion modes, ignore non-TextArtifact module results before ranking or merging. A duplicate means exact equality of `TextArtifact.value`. Keep the first artifact for a value in configured retrieval-module order and then module-result order, including that artifact's id, metadata, and reference.

In `concatenate` mode, return the remaining chunks in that same configured order and leave `retrieval_scores` empty. In `rrf` mode, each distinct value receives the sum of `weight / (rrf_k + rank)` across successful modules, with ranks starting at 1 among that module's TextArtifact results. Repeated values within one module contribute only their highest-ranked occurrence. A module omitted from `module_weights` has weight 1; an explicit zero weight is preserved and its candidates remain eligible with a zero contribution. Sort by descending fused score, breaking ties by first configured appearance. Store scores for every fused candidate before reranking or limiting, keyed by the retained artifact's id.

With `on_error="continue"`, skip failed retrieval modules in either fusion mode and record each failure under its module name as `"<ExceptionClass>: <message>"`; successful modules still contribute normally. With the default `"raise"`, propagate the original exception and do not replace the context's existing chunks or retrieval diagnostics.

Fusion happens before the optional rerank module. The rerank module receives all fused candidates, its returned TextArtifact order is authoritative, and `max_chunks` is applied afterward. `None` remains unbounded, a positive value keeps that many chunks, and zero produces an empty list.

Reject unsupported fusion/error modes with ValueError. Also reject a non-finite or non-positive `rrf_k`, any non-finite or negative module weight, and a negative `max_chunks` with ValueError.
