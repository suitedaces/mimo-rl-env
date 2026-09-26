Allow IterableDataset to be passed to LightningDataModule.from_datasets
## 🚀 Feature

Allow `IterableDataset` to be passed to `LightningDataModule.from_datasets`

### Motivation

Currently, we cannot pass `IterableDataset` instances to `LightningDataModule`'s `from_datasets` method.

This is because because `IterableDataset` cannot be used with `DataLoader` instances that are instantiated with `shuffle=True`. 

Right now, `DataLoader` instances created by `LightningDataModule` are hard-coded to set `shuffle=True`: 

https://github.com/PyTorchLightning/pytorch-lightning/blob/402a258705c10c8ad57bfdc16c39a8420b1425ee/pytorch_lightning/core/datamodule.py#L379

<!-- A clear and concise description of what you want to happen. -->

I think allowing users to pass a `shuffle` parameter to  `LightningDataModule.from_datasets` is a good idea.

<!-- A clear and concise description of any alternative solutions or features you've considered, if any. -->

### Additional context

<!-- Add any other context or screenshots about the feature request here. -->

I've made the code changes and am prepared to submit a pull request.
