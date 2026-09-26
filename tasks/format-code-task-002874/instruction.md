Log polluted by conda installer's progress bar
When installing SciPy with conda for the first time (using tox and tox-conda), the log file corresponding to the tox test environment creation contains carriage return characters on Linux.

Relevant section of **.tox/scipyenv/log/scipyenv-1.log**:
```
Downloading and Extracting Packages
^Mscipy-1.4.1          | 14.5 MB   |            |   0% 
^Mscipy-1.4.1          | 14.5 MB   |            |   0% 
^Mscipy-1.4.1          | 14.5 MB   |            |   0% 
^Mscipy-1.4.1          | 14.5 MB   | 1          |   1% 
^Mscipy-1.4.1          | 14.5 MB   | 1          |   2% 
```

This is probably a result of the progress bar of `conda install`.

I would expect the log to be concise so that it's easier to use for debugging.

**Details**
tox-conda 0.2.1
tox 3.14.6
conda 4.8.3

**Note**
When the tox test environment is re-created, for example by deleting the `.tox` directory and rerunning tox, the particular section of the log file that I mentioned above is missing. This might be due to conda caching, but I haven't verified this.
