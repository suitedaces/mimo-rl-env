## Simplify search-based insight type: drop the runtime / backend split

While working on the code insights module I keep hitting friction caused by the way search-based insights are typed today. `SearchBasedInsight` is a union of `SearchRuntimeBasedInsight` and `SearchBackendBasedInsight`, and the two variants have *different shapes*:

- `SearchRuntimeBasedInsight` has `repositories: string[]` but no `filters`
- `SearchBackendBasedInsight` has `filters: InsightFilters` but no `repositories`

Every place that touches a search-based insight ends up doing the same `if (insight.executionType === InsightExecutionType.Backend) { … } else { … }` dance to narrow which variant it has, and then has to remember which fields exist on which branch. A few examples I keep tripping over:

- `getSanitizedSearchInsight` returns one shape when `allRepos` is true and a *different* shape otherwise (with no filters at all).
- `getSearchInsightCreateInput` / `getSearchInsightUpdateInput` both have to guard on `executionType` before deciding what to put in `repositories` and whether to build a `filters` payload.
- `createInsightView` reconstructs the variant by inspecting `dataSeriesDefinitions[*].isCalculated` and then has to return two structurally different objects depending on the answer.
- `EditSearchBasedInsight` has two branches when building the form values, and the submit handler has to call `isSearchBackendBasedInsight` just to re-attach `filters` afterwards.
- Components like `BuiltInInsight` and `StandaloneRuntimeInsight` accept `SearchRuntimeBasedInsight | LangStatsInsight` as a prop, which only makes sense because of the split.

The thing is — in practice, the "runtime" variant for search-based insights doesn't really add anything the backend variant can't express. The backend pipeline already supports both "scoped to a list of repos" and "across all repos"; the runtime branch only exists because historically search-based insights with an explicit repo list ran in the FE. There's no product reason today for a search-based insight to require this two-variant typing — it just makes every file that touches it more complicated than it needs to be.

I'd like to collapse `SearchBasedInsight` into a single, unified type so that:

- there's one shape to consume everywhere (no more `executionType` narrowing just to figure out which fields are present),
- the same insight can carry both a repository scope and filter settings without callers having to special-case it, and
- the serializers, deserializer, and edit form stop having parallel branches that do almost the same thing.

The follow-on cleanup (removing the now-unused variant type, simplifying the components/forms/serializers that branched on it, and updating the relevant stories/mocks so they still typecheck) should fall out naturally once the type is unified.
