nDCG can not be called with float targets
## 🐛 Bug

Invoking `RetrievalNormalizedNDCG` & `retrieval_normalized_dcg` with target of type float results into
`ValueError: `target` must be a tensor of booleans or integers`

The reason is this [check in `_check_retrieval_functional_inputs`](https://github.com/PyTorchLightning/metrics/blob/21fe0ca7e1e61e197a923c6482c5fa07e32908de/torchmetrics/utilities/checks.py#L514):
```py
if target.dtype not in (torch.bool, torch.long, torch.int):
    raise ValueError("`target` must be a tensor of booleans or integers")
```



### To Reproduce

The code samples below are sufficient to reproduce the error

#### Code sample

Code sample for `retrieval_normalized_dcg`
```py
import torch
from torchmetrics.functional import retrieval_normalized_dcg

preds = torch.tensor([.1, .2, .3, 4, 70])
target = torch.tensor([0.1, 0, 0, 0.5, 1.0])
retrieval_normalized_dcg(preds, target)
```

Code sample for `RetrievalNormalizedNDCG`
```py
import torch
from torchmetrics import RetrievalNormalizedDCG

indexes =torch.tensor([0, 0, 0, 1, 1, 1, 1])
preds = torch.tensor([0.2, 0.3, 0.5, 0.1, 0.3, 0.5, 0.2])
target = torch.tensor([0.1, 0.1, 0.5, 0.5, 1.0, 1.0, 0.0])
ndcg = RetrievalNormalizedDCG()
ndcg(preds, target, indexes=indexes)
```

### Expected behavior

Targets of type float are handled without errors

### Environment

- PyTorch Version (e.g., 1.0): 1.9.0
- OS (e.g., Linux): Ubuntu 20.04
- How you installed PyTorch (`conda`, `pip`, source): source
- Build command you used (if compiling from source): `pip install git+git://github.com/PyTorchLightning/metrics.git@79cb5e2f1744b0d4cd3f15adf9d725a68452a50`
- Python version: 3.8.10
- CUDA/cuDNN version: N/A
- GPU models and configuration: N/A
- Any other relevant information: N/A
