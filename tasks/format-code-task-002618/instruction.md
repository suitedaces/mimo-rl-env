[OneHotEncoding constraint] Allow me to specify whether to keep the one-hot columns or collapse them into one categorical column
### Problem Description
The [OneHotEncoding constraint](https://docs.sdv.dev/sdv/concepts/constraint-augmented-generation-cag/predefined-constraints/onehotencoding) is meant to be used when you already have several one-hot encoded columns in your data. The constraint guarantees that the one-hot scheme will also be carried over into the synthetic data -- i.e. within each row, exactly 1 of the columns should contain a 1 while the rest should be 0.

Currently, the constraint works by keeping all the 0/1 columns for the ML model to learn. When creating synthetic data, it modifies the data so that only one column contains a `1` (and others contain a `0`). This strategy may not be optimal for a few reasons:

- **Performance**: If there are a lot of one-hot columns, the ML model's fitting and sampling time will be slow
- **Quality**: Some synthesizers are able to learn this type of data much better when it's presented as a single, discrete variable (categorical) rather than a set of one-hot columns

### Expected behavior
Add a parameter to this synthesizer called `learning_strategy`. This parameter can take on one of two values:
- (default) `'one_hot'`: The status quo. The AI will learn each of the one-hot columns, and the constraint will make sure that only one of the synthesized values is a `1`
- `'categorical'`: The constraint will collapse the one-hot columns into a single, categorical column for the AI model to learn. This may improve the performance (if you have a lot of one-hot columns), and quality (for certain synthesizers like GaussianCopula)
    - _Note that the final, outputted synthetic data should have the same 0/1 columns as the original data. (The promise is always that the synthetic data matches the format of the original.) The categorical column will just be created internally for the purposes of modeling; it should be reversed back into 0/1 columns when sampling._

```python
from sdv.cag import OneHotEncoding

constraint = OneHotEncoding(
  column_names=['status_new', 'status_on_hold', 'status_active', 'status_lapsed', 'status_churned'],
  learning_strategy='categorical'
)
```
