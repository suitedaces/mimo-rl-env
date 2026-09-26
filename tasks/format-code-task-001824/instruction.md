ValidationError: None is not of type 'string' while loading a trained model
**Describe the bug**
```sh
ValidationError: None is not of type 'string'

Failed validating 'type' in schema['properties']['input_features']['items']['allOf'][23]['then']['properties']['preprocessing']['properties']['char_vocab_file']:
    {'type': 'string'}

On instance['input_features'][0]['preprocessing']['char_vocab_file']:
    None
```

**To Reproduce**
Steps to reproduce the behavior:
1. Train the model with the following config
```python
from ludwig.api import LudwigModel
config = {
  "input_features": [{
    "name": "text",
    "type": "text",
    "level": 'word',
    "encoder": "rnn",
    "pretrained_embeddings": 'glove/glove.6B.300d.txt',
    "embedding_size": 300,
    "preprocessing": { "word_vocab_file": 'glove/glove.6B.300d.txt' }
  }],
  "output_features": [{ "name": "target", "type": "category" }],
  "training": {
    "decay": True,
    "learning_rate": 0.001,
    "validation_field": "target",
    "validation_metric": "accuracy"
  },
}
dataset_file_path = "../data/train.csv"
model = LudwigModel(config)
training_statistics, preprocessed_data, output_directory = model.train(dataset=dataset_file_path)
```
2. Load it with the ludwig api
```python
model = LudwigModel.load(os.path.join(output_directory, "model"))
```

**Expected behavior**
The model should be loaded without an error.

**Screenshots**
<img width="1351" alt="image" src="https://user-images.githubusercontent.com/4970420/135705934-46a8bc3c-4e5e-4b2b-a41e-5dfe94162810.png">


**Environment (please complete the following information):**
 - OS: [Ubuntu]
 - Version [18.04]
- Python version: 3.9
- Ludwig version: 0.4

**Additional context**
Trying to use Ludwig to solve a kaggle competition to get a taste of the entire workflow.
Here is the link to the dataset.
https://www.kaggle.com/c/nlp-getting-started/data

Thanks for the help!
