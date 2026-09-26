[BUG] inconsistency in the naming
### Is there an existing issue for this?

- [X] I have searched the existing issues

### Operating system

- [X] Linux
- [ ] Mac
- [ ] Windows

### Operating system version

For example one of the following:
- Linux Ubuntu 22.04
- Mac OS Version 12 "monterey"
- Windows 11


### Python version

- [ ] 3.12
- [ ] 3.11
- [X] 3.10
- [ ] 3.9
- [ ] 3.8

### nilearn version

dev version

### Expected behavior

The same argument has different names whether called in the `compute_contrast` function of the corresponding method of the *GLM classes.
`contrast_type`  in the function, see  https://github.com/nilearn/nilearn/blob/cfc4c03f/nilearn/glm/contrasts.py#L66
`stat_type` in teh method, see https://github.com/nilearn/nilearn/blob/cfc4c03fe2533dfffd6a6f034f1d6404262e1ec1/nilearn/glm/first_level/first_level.py#L763C9-L763C9
We should  deprecate one of them. 
My imrpession is that `stat_type` is more accurate.

### Current behavior & error messages

This is what I got:



```bash
# Paste the error message here


```


### Steps and code to reproduce bug

```python
# Paste your code here


```
