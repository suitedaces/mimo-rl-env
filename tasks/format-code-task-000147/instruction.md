Deprecate `LightningLoggerBase.close`
## Proposed refactoring or deprecation

<!-- A clear and concise description of the code improvement -->

### Motivation

This is a follow up to https://github.com/PyTorchLightning/pytorch-lightning/discussions/9004#discussioncomment-1212966
and
https://github.com/PyTorchLightning/pytorch-lightning/issues/9037

The base logger API has `close` defined
https://github.com/PyTorchLightning/pytorch-lightning/blob/089ae9b3e82ddc31942e315294e31e48c0a899db/pytorch_lightning/loggers/base.py#L312-L314

This is only implemented on https://github.com/PyTorchLightning/pytorch-lightning/blob/089ae9b3e82ddc31942e315294e31e48c0a899db/pytorch_lightning/loggers/test_tube.py#L197-L204

Given the test tube logger has since been deprecated, we can also deprecate this method off the base API as it's very unclear what the difference is between save/close/finalize currently. 

This function is never called by the Trainer either, so deprecating it from the base logger API has minimal changes for users.

<!-- Please outline the motivation for the proposal. If this is related to another GitHub issue, please link here too -->

### Pitch

- Deprecate `close` off the base API in v1.5
- Remove it from the API in v1.7

<!-- A clear and concise description of what you want to happen. -->

### Additional context

<!-- Add any other context or screenshots here. -->

______________________________________________________________________

#### If you enjoy Lightning, check out our other projects! ⚡

<sub>

- [**Metrics**](https://github.com/PyTorchLightning/metrics): Machine learning metrics for distributed, scalable PyTorch applications.

- [**Flash**](https://github.com/PyTorchLightning/lightning-flash): The fastest way to get a Lightning baseline! A collection of tasks for fast prototyping, baselining, finetuning and solving problems with deep learning

- [**Bolts**](https://github.com/PyTorchLightning/lightning-bolts): Pretrained SOTA Deep Learning models, callbacks and more for research and production with PyTorch Lightning and PyTorch

- [**Lightning Transformers**](https://github.com/PyTorchLightning/lightning-transformers): Flexible interface for high performance research using SOTA Transformers leveraging Pytorch Lightning, Transformers, and Hydra.

</sub>
