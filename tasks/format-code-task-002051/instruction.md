FirstLevelModel fit method could raise warning when confounds and design_matrices are specified together.
Hi,

I recently used `FirstLevelModel` in my project and discovered a mistake I made that was quite hard to detect. I was using custom design matrix and fitted model instance like this:
```python
first_level_model.fit(imgs, confounds=confounds, design_matrices=dm)
``` 
and didn't realize that in this case confounds would not be used. I noticed that few weeks later when I tried different confounds and see no difference in the images (because in both cases they were not used). I then read the documentation about `design_matrices` arg and found this statement: "If given it takes precedence over events and confounds.". 

I thought it would be nice to add warning if user call fit method just like me to let him know that something is wrong. It's just a few lines of code, but maybe will help someone who didn't read the documentation carefully like me.

Tell me what you think.
