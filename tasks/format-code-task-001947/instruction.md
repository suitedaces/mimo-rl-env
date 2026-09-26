Resampling to the identical frequency
### Description of the problem

Resampling of a continuous signal proceeds even if the signal already has the desired new frequency.

### Steps to reproduce

```Python
raw = mne.io.read_raw()
raw.resample(250)
raw.resample(250)
```


### Link to data

_No response_

### Expected results

The resample() function doesn't proceed and doesn't modify the object if it's already has the desired frequency.

### Actual results

Resampling runs again.

### Additional information

```
Platform             Windows-10-10.0.20348-SP0
Python               3.11.3 (tags/v3.11.3:f3909b8, Apr  4 2023, 23:49:59) [MSC v.1934 64 bit (AMD64)]
Executable           C:\Users\Gennadiy\Documents\proj\.venv\Scripts\python.exe
CPU                  Intel64 Family 6 Model 167 Stepping 1, GenuineIntel (16 cores)
Memory               127.9 GB

Core
├☑ mne               1.4.2
├☑ numpy             1.23.5 (OpenBLAS 0.3.20 with 16 threads)
├☑ scipy             1.10.1
├☑ matplotlib        3.7.1 (backend=QtAgg)
├☑ pooch             1.7.0
└☑ jinja2            3.1.2

Numerical (optional)
├☑ sklearn           1.2.2
├☑ numba             0.57.0
├☑ cupy              12.1.0
├☑ pandas            2.0.2
└☐ unavailable       nibabel, nilearn, dipy, openmeeg

Visualization (optional)
├☑ qtpy              2.3.1 (PyQt5=5.15.2)
├☑ ipympl            0.9.3
├☑ pyqtgraph         0.13.3
├☑ mne-qt-browser    0.5.0
└☐ unavailable       pyvista, pyvistaqt, ipyvtklink, vtk

Ecosystem (optional)
└☐ unavailable       mne-bids, mne-nirs, mne-features, mne-connectivity, mne-icalabel, mne-bids-pipeline
```
