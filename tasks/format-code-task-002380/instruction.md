SQ elements return wrong VM
[SQ elements always have a VM of 1](http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_7.5.html), however:
```python
>>> from pydicom import Dataset
>>> ds = Dataset()
>>> ds.BeamSequence = [Dataset(), Dataset()]
>>> ds["BeamSequence"].VM
2
```
From what I understand, this is also the case for an empty sequence, which is really annoying from a usage point of view. It seems like the value is the "sequence", which may or may not contain items. 

Technically this is understandable as the DICOM Standard doesn't conflate a SQ element's sequence with a non-SQ element's multi-value, but in pydicom they're both represented as `MutableSequence`, so it may be a bit confusing as a naive user probably expects the same behaviour in both cases.

Still, I think it'd make sense to follow the Standard's VM definition here and deal with any user confusion. The Standard is pretty explicit.
