## Problem Statement

Hey, I'm trying to benchmark some GNN stuff on the Geom-GCN node classification datasets and I noticed dgl ships Cora/Citeseer/Pubmed and a bunch of others out of the box but not Chameleon. Could you add a built-in `ChameleonDataset` under `dgl.data` (the Wikipedia page-page network, Geom-GCN variant with the 10 standard train/val/test splits) so I can just import it and grab the graph the same way I do with the other built-ins? Would save me from rolling my own loader every time.

## Expected Outcomes

- Dataset availability:
  - `dgl.data.ChameleonDataset` is importable and instantiable in the same style as other built-in DGL datasets, including the usual dataset options such as raw data location, reload control, verbosity, and graph transform.
  - A `ChameleonDataset` instance behaves as a single-graph node classification dataset: its length is one, and indexing the dataset returns the Chameleon graph.
  - The returned graph represents the Geom-GCN Chameleon dataset and supports the standard DGL graph and node-data access patterns used by other built-in node classification datasets.
  - The new dataset is discoverable from the DGL data API documentation alongside the other node classification/regression datasets.

- Graph data format:
  - The graph exposes node features through `g.ndata["feat"]` as floating-point data.
  - The graph exposes node labels through `g.ndata["label"]` as integer class labels.
  - `dataset.num_classes` reports the number of label classes and is consistent with the labels stored on the graph.
  - The graph exposes `g.ndata["train_mask"]`, `g.ndata["val_mask"]`, and `g.ndata["test_mask"]`; these are boolean node masks containing the standard 10 Geom-GCN train/validation/test splits as columns.

- Dataset loading and cache behavior:
  - Loading Chameleon in an environment where the required PyTorch backend support is unavailable fails clearly with `ModuleNotFoundError` indicating that PyTorch is required as the backend.
  - Built-in datasets with a configured source URL use cache locations that are distinct per source URL, so changing the source does not accidentally reuse stale raw or processed data from a previous source.
  - Datasets without a configured source URL keep their previous cache-directory behavior.
  - Existing built-in datasets that rely on a single downloaded raw artifact continue to locate and load their expected raw files correctly after the cache-location change.

## Implementation Notes

The concrete parsing structure, helper classes, cache-key implementation, and validation placement are up to the implementer. Match the public DGL dataset conventions and keep assertions focused on externally observable dataset behavior rather than any particular internal organization.
