Deprecate {train/val/test}_transforms, dims, and size from the DataModule
## 🚀 Feature

Deprecate these properties off the LightningDataModule interface:
https://github.com/PyTorchLightning/pytorch-lightning/blob/963c26764682fa4cf64c93c5a7572ae0040e9c32/pytorch_lightning/core/datamodule.py#L94-L147

### Motivation

We are auditing the Lightning components and APIs to assess opportunities for improvements:
- https://docs.google.com/document/d/1xHU7-iQSpp9KJTjI3As2EM0mfNHHr37WZYpDpwLkivA/edit#
- https://github.com/PyTorchLightning/pytorch-lightning/issues/7740#issuecomment-876780318

`train_transforms`, `val_transforms`, `test_transforms`, `dims`, and `size` are entirely optional to use, yet they’re on the DataModule interface. The Trainer does not rely on these, nor is the user forced to implement them. In reality, these are internal implementation details of individual datamodules. As a result, we ought to deprecate these off the DataModule interface.

Of course, users retain the ability to implement these properties in their LightningModules if they find these abstractions helpful.

<!-- Please outline the motivation for the proposal. Is your feature request related to a problem? e.g., I'm always frustrated when [...]. If this is related to another GitHub issue, please link here too -->

### Pitch

We can follow a similar approach as what was done for https://github.com/PyTorchLightning/pytorch-lightning/issues/7301
- Mark the properties as deprecated in v1.5. Warn if users are passing non-None values to the DataModule constructor and if they read/set their corresponding properties
- Remove the properties in v1.7

<!-- A clear and concise description of what you want to happen. -->

### Alternatives
Keep as is

<!-- A clear and concise description of any alternative solutions or features you've considered, if any. -->

### Additional context

<!-- Add any other context or screenshots about the feature request here. -->

______________________________________________________________________

#### If you enjoy Lightning, check out our other projects! ⚡

<sub>

- [**Metrics**](https://github.com/PyTorchLightning/metrics): Machine learning metrics for distributed, scalable PyTorch applications.

- [**Flash**](https://github.com/PyTorchLightning/lightning-flash): The fastest way to get a Lightning baseline! A collection of tasks for fast prototyping, baselining, finetuning and solving problems with deep learning

- [**Bolts**](https://github.com/PyTorchLightning/lightning-bolts): Pretrained SOTA Deep Learning models, callbacks and more for research and production with PyTorch Lightning and PyTorch

- [**Lightning Transformers**](https://github.com/PyTorchLightning/lightning-transformers): Flexible interface for high performance research using SOTA Transformers leveraging Pytorch Lightning, Transformers, and Hydra.

</sub>
