EarlyStopping is based upon callback.on_train_epoch_end, not callback.on_validation_epoch_end
## 🐛 Bug

[EarlyStopping](https://pytorch-lightning.readthedocs.io/en/latest/common/early_stopping.html) patience is supposed to be based upon `callback.on_validation_epoch_end`. "It must be noted that the patience parameter counts the number of validation epochs with no improvement, and not the number of training epochs. Therefore, with parameters check_val_every_n_epoch=10 and patience=3, the trainer will perform at least 40 training epochs before being stopped."

However, if you set `check_val_every_n_epoch=10` and `patience=3`, you will get a crash after the first training epoch because of `callback.on_train_epoch_end`:

```
Traceback (most recent call last):
  File "/usr/lib/python3.7/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/usr/lib/python3.7/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/workspace/project/heareval/predictions/runner.py", line 75, in <module>
    runner()
  File "/usr/local/lib/python3.7/dist-packages/click/core.py", line 1137, in __call__
    return self.main(*args, **kwargs)
  File "/usr/local/lib/python3.7/dist-packages/click/core.py", line 1062, in main
    rv = self.invoke(ctx)
  File "/usr/local/lib/python3.7/dist-packages/click/core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/usr/local/lib/python3.7/dist-packages/click/core.py", line 763, in invoke
    return __callback(*args, **kwargs)
  File "/workspace/project/heareval/predictions/runner.py", line 70, in runner
    task_path, scene_embedding_size, timestamp_embedding_size, gpus
  File "/workspace/project/heareval/predictions/task_predictions.py", line 764, in task_predictions
    gpus=gpus,
  File "/workspace/project/heareval/predictions/task_predictions.py", line 646, in task_predictions_train
    trainer.fit(predictor, train_dataloader, valid_dataloader)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/trainer/trainer.py", line 553, in fit
    self._run(model)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/trainer/trainer.py", line 918, in _run
    self._dispatch()
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/trainer/trainer.py", line 986, in _dispatch
    self.accelerator.start_training(self)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/accelerators/accelerator.py", line 92, in start_training
    self.training_type_plugin.start_training(trainer)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/plugins/training_type/training_type_plugin.py", line 161, in start_training
    self._results = trainer.run_stage()
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/trainer/trainer.py", line 996, in run_stage
    return self._run_train()
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/trainer/trainer.py", line 1045, in _run_train
    self.fit_loop.run()
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/loops/base.py", line 111, in run
    self.advance(*args, **kwargs)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/loops/fit_loop.py", line 200, in advance
    epoch_output = self.epoch_loop.run(train_dataloader)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/loops/base.py", line 118, in run
    output = self.on_run_end()
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/loops/epoch/training_epoch_loop.py", line 235, in on_run_end
    self._on_train_epoch_end_hook(processed_outputs)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/loops/epoch/training_epoch_loop.py", line 276, in _on_train_epoch_end_hook
    trainer_hook(processed_epoch_output)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/trainer/callback_hook.py", line 109, in on_train_epoch_end
    callback.on_train_epoch_end(self, self.lightning_module)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/callbacks/early_stopping.py", line 170, in on_train_epoch_end
    self._run_early_stopping_check(trainer)
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/callbacks/early_stopping.py", line 185, in _run_early_stopping_check
    logs
  File "/usr/local/lib/python3.7/dist-packages/pytorch_lightning/callbacks/early_stopping.py", line 134, in _validate_condition_metric
    raise RuntimeError(error_msg)
RuntimeError: Early stopping conditioned on metric `val_event_onset_200ms_fms` which is not available. Pass in or modify your `EarlyStopping` callback to use any of the following: `train_loss`
```

### To Reproduce

BoringModel replication:

https://colab.research.google.com/drive/1MsMGM7Wsi6wJ50cIhn1jvxOaVg8z_Ypl#scrollTo=Flyi--SpvsJN

### Expected behavior

It should only do early stopping callback on validation epoch ends, not training epoch ends.

### Environment


    CUDA:
        GPU:
        available: False
        version: None
    Packages:
        numpy: 1.19.5
        pyTorch_debug: False
        pyTorch_version: 1.9.0
        pytorch-lightning: 1.4.1
        tqdm: 4.62.0
    System:
        OS: Darwin
        architecture:
            64bit
        processor: i386
        python: 3.9.6
        version: Darwin Kernel Version 19.6.0: Tue Jun 22 19:49:55 PDT 2021; root:xnu-6153.141.35~1/RELEASE_X86_64
