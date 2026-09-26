Possible BUG - fir_design/firwin breaking filtering routine
Started hitting this error after updating master to recent upstream. @larsoner suspected a bug. Currently, I am on commit b33a26. `fir_design = 'firwin'` seems to be breaking the filtering routine. I was able to reproduce with sample data using...

```
from mne.datasets import sample
filter_length = '5s'
fir_design = 'firwin'
fir_window = 'hann'
h_freq = 55
h_trans_bandwidth = 0.5
iir_params = None
l_freq = None
l_trans_bandwidth = 0.5
method = 'fir'
phase = 'zero-double'
pad = 'reflect_limited'

data_path = sample.data_path()
fname = data_path + '/MEG/sample/sample_audvis_raw.fif'
raw = mne.io.read_raw_fif(fname, preload=True)
raw.filter(l_freq=l_freq, h_freq=h_freq, filter_length=filter_length,
           l_trans_bandwidth=l_trans_bandwidth,
           h_trans_bandwidth=h_trans_bandwidth, method=method,
           iir_params=iir_params, phase=phase,
           fir_window=fir_window, fir_design=fir_design, pad=pad, verbose=True)

```

Trace...

> Traceback (most recent call last):
>   File "/home/ktavabi/miniconda3/envs/py2.7/lib/python2.7/site-packages/IPython/core/interactiveshell.py", line 2881, in run_code
>     exec(code_obj, self.user_global_ns, self.user_ns)
>   File "<ipython-input-2-07360ce66dba>", line 23, in <module>
>     fir_window=fir_window, fir_design=fir_design, pad=pad, verbose=True)
>   File "<string>", line 2, in filter
>   File "/home/ktavabi/Projects/mne-python/mne/utils.py", line 727, in verbose
>     return function(*args, **kwargs)
>   File "/home/ktavabi/Projects/mne-python/mne/io/base.py", line 1251, in filter
>     fir_window=fir_window, fir_design=fir_design, pad=pad)
>   File "<string>", line 2, in filter_data
>   File "/home/ktavabi/Projects/mne-python/mne/utils.py", line 728, in verbose
>     return function(*args, **kwargs)
>   File "/home/ktavabi/Projects/mne-python/mne/filter.py", line 862, in filter_data
>     h_trans_bandwidth, method, iir_params, phase, fir_window, fir_design)
>   File "<string>", line 2, in create_filter
>   File "/home/ktavabi/Projects/mne-python/mne/utils.py", line 728, in verbose
>     return function(*args, **kwargs)
>   File "/home/ktavabi/Projects/mne-python/mne/filter.py", line 1159, in create_filter
>     fir_window, fir_design)
>   File "/home/ktavabi/Projects/mne-python/mne/filter.py", line 399, in _construct_fir_filter
>     h = fir_design(N, freq, gain, window=fir_window)
>   File "/home/ktavabi/Projects/mne-python/mne/filter.py", line 331, in _firwin_design
>     h[offset:N - offset] += this_h
> ValueError: operands could not be broadcast together with shapes (3726,) (3725,) (3726,)
