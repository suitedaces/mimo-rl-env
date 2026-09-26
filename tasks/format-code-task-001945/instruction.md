mne.time_frequency.psd_welch with option average=median
In the function `mne.time_frequency.psd_welch`, for the option `average` it is written:
_How to average the segments. If mean (default), calculate the arithmetic mean. If median, calculate the median, corrected for its bias relative to the mean. If None, returns the unaggregated segments._

I searched through the code, and am not finding any correction of the median for the bias relative to mean.
1. Is it actually done somewhere and I missed?
2. Would you have some references about how such bias correction is done?
