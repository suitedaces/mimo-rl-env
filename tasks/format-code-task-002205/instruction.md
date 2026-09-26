BUG: non-standard frequency Period arithmetic
#### Code Sample

```python
starting_date = pd.Period('20180101', freq='24H') 
base_date = pd.Period('19700101', freq='24H')
offset = starting_date - base_date
base_date + offset == starting_date  # -> False   should be True
base_date + offset == (pd.Period(str(base_date), freq='H') + (24*offset)).asfreq('24H')  # -> True  This is how it's actually being processed now
(pd.Period(str(base_date), freq='H') + offset).asfreq('24H') == starting_date  # -> True  This is what needs to be done now to get the desired result
```
#### Problem description
In short: (A - B) + B != A

The result of diffing two periods of a scaled frequency is represented in the number of periods of the base frequency, not the scaled frequency. Thus when adding back to the scaled frequency the resulting Period will be N (where N is the scaling factor) times more periods than should be added.


The 2 options that don't involve some sort of custom delta object don't really work well:

1) offset divided by the scaling factor
  - This would not work for some scaling factors (e.g. '5H').
2) adding an int to a Period should not scale the int by the scaling factor, but rather just add that number of base periods.
  - This breaks the logic that, for example,  pd.Period('19700101', freq='3H') + 1 == pd.Period('19700101 03:00', freq='3H'), which I don't think should be compromised

#### Suggestion:

A simple PeriodDelta object that just contains (int, freq), where the int is the current resulting int. When added to a period, if the frequency matches the PeriodDelta freq, then the Period will be cast to it's base frequency the int added and then cast back. Ints will still be valid input, but the difference of Periods could return this object instead.

#### Output of ``pd.show_versions()``

v0.23.4
