ENH: Allow recursive estimation for samp size less than window size in RollingOLS
#### Is your feature request related to a problem? Please describe
Sometimes you want estimates for sample sizes smaller than the full window size. 


#### Describe the solution you'd like
Allow recursive estimation before the full sample is reached in RollingOLS so that the window would be
```
[1,n1]
[1,n1+2]
...
[1,window]
[2,window+1]
....
```

This is expanding window until the full window length is reached.
