LitProgressBar ignores TQDM_MINITERS
### Bug description

tqdm supports setting the environment variable `TQDM_MINITERS` to reduce the frequency of progress bar updates.
Since lightning trainer defaults to a TQDM progress bar, I expected this to work for lightning. However, pytorch lightnings trainer seems to ignore this.

### What version are you seeing the problem on?

v2.1

### How to reproduce the bug

```python
export TQDM_MINITERS=5
python your_script.py


where script can be anything using a `pytorch_lightning.Trainer` with `progress_bar_enabled=True`
```


### Error messages and logs


-

### Environment

<details>
  <summary>Current environment</summary>

```
#- Lightning Component (e.g. Trainer, LightningModule, LightningApp, LightningWork, LightningFlow): Trainer
#- PyTorch Lightning Version (e.g., 1.5.0): 2.1.3
#- Lightning App Version (e.g., 0.5.2):
#- PyTorch Version (e.g., 2.0): 2.0.1
#- Python version (e.g., 3.9): 3.9
#- OS (e.g., Linux): Linux
#- CUDA/cuDNN version:
#- GPU models and configuration:
#- How you installed Lightning(`conda`, `pip`, source): poetry
#- Running environment of LightningApp (e.g. local, cloud):
```

</details>


### More info

_No response_

cc @awaelchli
