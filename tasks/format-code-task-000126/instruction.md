# Problem Statement

I'm trying to train the conf_branch method with a resnet18 backbone on CIFAR and it blows up with a shape mismatch as soon as it hits the forward pass. The configs/train_conf_branch.yml as-is doesn't seem to work for anything other than whatever tiny backbone it was originally written against. Also while poking around I noticed `postprocessor.name: opengan` just throws a KeyError saying it's not registered, and `trainer.name: opengan` only works if I spell it `openGan` which is weird. Can you take a look at the conf_branch + opengan pipelines end to end?

# Expected outcomes

- The conf_branch network wrapper should run a forward pass successfully with compatible CIFAR-style ResNet backbones and other compatible backbones with nontrivial feature/output dimensions.
- `ConfBranchNet.forward(x)` should produce class predictions with shape `(batch_size, num_classes)`.
- `ConfBranchNet.forward(x, return_confidence=True)` should return both class predictions and confidence scores, with confidence shaped `(batch_size, 1)`.
- The conf_branch training configuration should use a recorder that is available through the normal configuration-driven recorder construction path so that the training pipeline can be constructed from the provided config.
- `get_postprocessor` should accept `config.postprocessor.name: opengan` and construct the OpenGAN postprocessor.
- `get_trainer` should accept `config.trainer.name: opengan` using the same lowercase spelling used in OpenGAN configs.
- Conf_branch training epoch metrics should include the training loss in addition to accuracy and epoch index.

# Implementation notes

- The exact internal wiring, helper structure, and validation locations are up to the implementer.
- Prefer behavior-compatible fixes that preserve existing public APIs and configuration-driven construction patterns.
- Do not special-case a single backbone or dataset; the conf_branch path should work for compatible backbones that expose the representation needed by the wrapper.
