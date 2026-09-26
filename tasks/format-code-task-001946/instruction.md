`SlidingEstimator` seems to ignore `verbose=False` (especially when n_jobs > 1)
### Description of the problem

`SlidingEstimator` seems to ignore `verbose=False` when n_jobs > 1. This happens during `.fit()` and `.score()` and leads to progress bar showing up and multiple messages in the console:
```
  0%|          | Fitting SlidingEstimator : 0/100 [00:00<?,       ?it/s]
[Parallel(n_jobs=10)]: Using backend LokyBackend with 10 concurrent workers.
[Parallel(n_jobs=10)]: Done   4 out of  10 | elapsed:    0.0s remaining:    0.0s
[Parallel(n_jobs=10)]: Done   7 out of  10 | elapsed:    0.0s remaining:    0.0s
[Parallel(n_jobs=10)]: Done  10 out of  10 | elapsed:    0.0s remaining:    0.0s
[Parallel(n_jobs=10)]: Done  10 out of  10 | elapsed:    0.0s finished
```
When the estimators are fit many times (for example when calculating randomization control or processing multiple subjects) this leads to many, many messages in the console.

### Steps to reproduce

```Python
import numpy as np
from sklearn.svm import SVC
import mne

data = np.random.random((40, 20, 100))
classes = np.random.randint(0, 2, size=40)
clf = SVC()

# %% shows only the progress bar when n_jobs=1
estimator = mne.decoding.SlidingEstimator(clf, n_jobs=1, verbose=False)
estimator.fit(data, classes)
scores = estimator.score(data, classes)

# %% shows progress bar and prints other messages to the console
estimator = mne.decoding.SlidingEstimator(clf, n_jobs=10, verbose=False)
estimator.fit(data, classes)
scores = estimator.score(data, classes)
```


### Link to data

_No response_

### Expected results

Nothing printed to the console when `verbose=False`.

### Actual results

```
  0%|          | Fitting SlidingEstimator : 0/100 [00:00<?,       ?it/s]
[Parallel(n_jobs=10)]: Using backend LokyBackend with 10 concurrent workers.
[Parallel(n_jobs=10)]: Done   4 out of  10 | elapsed:    0.0s remaining:    0.0s
[Parallel(n_jobs=10)]: Done   7 out of  10 | elapsed:    0.0s remaining:    0.0s
[Parallel(n_jobs=10)]: Done  10 out of  10 | elapsed:    0.0s remaining:    0.0s
[Parallel(n_jobs=10)]: Done  10 out of  10 | elapsed:    0.0s finished
```

### Additional information

```
mne.sys_info()
Platform:         Windows-10-10.0.19045-SP0
Python:           3.9.6 | packaged by conda-forge | (default, Jul 11 2021, 03:37:25) [MSC v.1916 64 bit (AMD64)]
Executable:       C:\Users\mmagnuski\anaconda3\envs\mne\python.exe
CPU:              Intel64 Family 6 Model 85 Stepping 7, GenuineIntel: 24 cores
Memory:           127.7 GB

mne:              1.3.0
numpy:            1.20.3 {MKL 2020.0.4 with 12 threads}
scipy:            1.7.1
matplotlib:       3.4.2 {backend=module://matplotlib_inline.backend_inline}

sklearn:          0.24.2
numba:            0.53.1
nibabel:          3.2.1
nilearn:          0.8.0
dipy:             1.4.1
openmeeg:         Not found
cupy:             Not found
pandas:           1.3.1
pyvista:          0.31.3 {OpenGL 4.5.0 NVIDIA 516.94 via NVIDIA GeForce GTX 1660 SUPER/PCIe/SSE2}
pyvistaqt:        0.5.0
ipyvtklink:       0.2.1
vtk:              9.0.1
qtpy:             2.2.1 {PyQt5=5.12.9}
ipympl:           Not found
pyqtgraph:        0.12.3
pooch:            v1.6.0

mne_bids:         Not found
mne_nirs:         Not found
mne_features:     Not found
mne_qt_browser:   Not found
mne_connectivity: Not found
mne_icalabel:     Not found
```
