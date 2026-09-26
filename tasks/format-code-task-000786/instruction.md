# Add a corpus shuffling-and-splitting utility for streaming data loading

When we train a language model from scratch we feed the trainer with a `StreamingDataSilo`, which
reads training data lazily from disk instead of loading everything into memory. To get good
randomization across epochs with that streaming setup it helps to pre-process the raw corpus once:
break one huge text file into many smaller files and shuffle the lines as we go, so the streaming
loader can read (and optionally further shuffle) those parts in arbitrary order.

Please add this pre-processing helper to the data-handling utilities so it can be imported as:

```python
from farm.data_handler.utils import randomize_and_split_file
```

The corpus format is the usual one we already use elsewhere: one sentence per line, with documents
separated by a *delimiter* line (by default an empty line).

## Behavior

`randomize_and_split_file(filepath, output_dir, docs_per_file=1000, delimiter="", encoding="utf-8")`

- Reads the text corpus at `filepath` and writes the result as several files inside `output_dir`.
- `output_dir` must be created automatically if it does not already exist (including any missing
  parent directories).
- Documents are delimited by lines that, once stripped of surrounding whitespace, equal
  `delimiter`. With the default (`""`) that means blank lines separate documents. A custom
  `delimiter` such as `"[DOC_SEP]"` must be honoured instead of blank lines.
- The documents are written out grouped into the output files such that each output file holds at
  most `docs_per_file` documents. Consequently, when the corpus contains a number of documents that
  is an exact multiple of `docs_per_file`, exactly `num_documents / docs_per_file` files are
  produced; a corpus whose document count does not exceed `docs_per_file` is written to a single
  file. Smaller `docs_per_file` therefore yields more output files.
- The split must be loss-less: every line of the input — including the delimiter lines themselves —
  appears exactly once across the produced files, with no lines added, dropped or altered.
- The lines are shuffled: the order of lines emitted is randomized rather than preserved from the
  input.

`filepath` and `output_dir` may be given as strings or `pathlib.Path` objects.
