Using `.crop()` on mff dataset leads to errors later on
The problem happens when doing `events = mne.find_events(raw)` or `raw.load_data()` when the raw file was previously cropped, for example:
```python
import mne

fname = 'some_file.mff'
raw = mne.io.read_raw_egi(fname)
raw.crop(tmin=2.5)
```

now both:
```python
events = mne.find_events(raw)
```
and:
```python
raw.load_data()
```
lead to the same error. Both errors are the same starting from `_read_segment_file` but I paste both below.
for `mne.find_events(raw)`:
```python-traceback
<c:\src\mne-python\mne\externals\decorator.py:decorator-gen-129> in find_events(raw, stim_channel, output, consecutive, min_duration, shortest_event, mask, uint_cast, mask_type, initial_event, verbose)

c:\src\mne-python\mne\utils\_logging.py in wrapper(*args, **kwargs)
     87             with use_log_level(verbose_level):
     88                 return function(*args, **kwargs)
---> 89         return function(*args, **kwargs)
     90     return FunctionMaker.create(
     91         function, 'return decfunc(%(signature)s)',

c:\src\mne-python\mne\event.py in find_events(raw, stim_channel, output, consecutive, min_duration, shortest_event, mask, uint_cast, mask_type, initial_event, verbose)
    684     if len(picks) == 0:
    685         raise ValueError('No stim channel found to extract event triggers.')
--> 686     data, _ = raw[picks, :]
    687 
    688     events_list = []

c:\src\mne-python\mne\io\base.py in __getitem__(self, item)
    887             data = self._read_segment(start=start, stop=stop, sel=sel,
    888                                       projector=self._projector,
--> 889                                       verbose=self.verbose)
    890         times = self.times[start:stop]
    891         return data, times

c:\src\mne-python\mne\io\base.py in _read_segment(self, start, stop, sel, data_buffer, projector, verbose)
    541             self._read_segment_file(data[:, this_sl], idx, fi,
    542                                     int(start_file), int(stop_file),
--> 543                                     cals, mult)
    544             offset += n_read
    545         return data

c:\src\mne-python\mne\io\egi\egimff.py in _read_segment_file(self, data, idx, fi, start, stop, cals, mult)
    508             # Start reading samples
    509             while samples_to_read > 0:
--> 510                 this_block_info = _block_r(fid)
    511                 if this_block_info is not None:
    512                     current_block_info = this_block_info

c:\src\mne-python\mne\io\egi\general.py in _block_r(fid)
    141 def _block_r(fid):
    142     """Read meta data."""
--> 143     if np.fromfile(fid, dtype=np.dtype('i4'), count=1)[0] != 1:  # not metadata
    144         return None
    145     header_size = np.fromfile(fid, dtype=np.dtype('i4'), count=1)[0]

IndexError: index 0 is out of bounds for axis 0 with size 0
```

for `raw.load_data()`:
```python-traceback
<c:\src\mne-python\mne\externals\decorator.py:decorator-gen-132> in load_data(self, verbose)

c:\src\mne-python\mne\utils\_logging.py in wrapper(*args, **kwargs)
     87             with use_log_level(verbose_level):
     88                 return function(*args, **kwargs)
---> 89         return function(*args, **kwargs)
     90     return FunctionMaker.create(
     91         function, 'return decfunc(%(signature)s)',

c:\src\mne-python\mne\io\base.py in load_data(self, verbose)
    631         """
    632         if not self.preload:
--> 633             self._preload_data(True)
    634         return self
    635 

<c:\src\mne-python\mne\externals\decorator.py:decorator-gen-133> in _preload_data(self, preload, verbose)

c:\src\mne-python\mne\utils\_logging.py in wrapper(*args, **kwargs)
     87             with use_log_level(verbose_level):
     88                 return function(*args, **kwargs)
---> 89         return function(*args, **kwargs)
     90     return FunctionMaker.create(
     91         function, 'return decfunc(%(signature)s)',

c:\src\mne-python\mne\io\base.py in _preload_data(self, preload, verbose)
    641         logger.info('Reading %d ... %d  =  %9.3f ... %9.3f secs...' %
    642                     (0, len(self.times) - 1, 0., self.times[-1]))
--> 643         self._data = self._read_segment(data_buffer=data_buffer)
    644         assert len(self._data) == self.info['nchan']
    645         self.preload = True

c:\src\mne-python\mne\io\base.py in _read_segment(self, start, stop, sel, data_buffer, projector, verbose)
    541             self._read_segment_file(data[:, this_sl], idx, fi,
    542                                     int(start_file), int(stop_file),
--> 543                                     cals, mult)
    544             offset += n_read
    545         return data

c:\src\mne-python\mne\io\egi\egimff.py in _read_segment_file(self, data, idx, fi, start, stop, cals, mult)
    508             # Start reading samples
    509             while samples_to_read > 0:
--> 510                 this_block_info = _block_r(fid)
    511                 if this_block_info is not None:
    512                     current_block_info = this_block_info

c:\src\mne-python\mne\io\egi\general.py in _block_r(fid)
    141 def _block_r(fid):
    142     """Read meta data."""
--> 143     if np.fromfile(fid, dtype=np.dtype('i4'), count=1)[0] != 1:  # not metadata
    144         return None
    145     header_size = np.fromfile(fid, dtype=np.dtype('i4'), count=1)[0]

IndexError: index 0 is out of bounds for axis 0 with size 0
```

I'm on master, but had this problem 3 months ago too.
`preload=True` when reading eliminates the issue, but it would be nice if `preload` was not necessary.
