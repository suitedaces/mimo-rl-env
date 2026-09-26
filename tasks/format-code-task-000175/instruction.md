[Bug]: regression in 2.3.0 leading to IndexError
### What happened?

original report https://github.com/dandi/dandi-cli/issues/1223 for test failing while working on data from https://github.com/dandisets/nwb_test_data/tree/master/v2.0.1 



### Steps to Reproduce

```python
see below in traceback demo
```


### Traceback

```python
❯ python -c 'from dandi.metadata import get_metadata; print(get_metadata("/home/yoh/proj/dandi/nwb-datasets/nwb_test_data/v2.0.1/test_Subject.nwb"))'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/fscacher/cache.py", line 152, in fingerprinter
    ret = fingerprinted(*args, **kwargs_)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/joblib/memory.py", line 594, in __call__
    return self._cached_call(args, kwargs)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/joblib/memory.py", line 537, in _cached_call
    out, metadata = self.call(*args, **kwargs)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/joblib/memory.py", line 779, in call
    output = self.func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/fscacher/cache.py", line 98, in fingerprinted
    return f(path, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/dandi/metadata.py", line 131, in get_metadata
    meta.update(_get_pynwb_metadata(path))
                ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/dandi/pynwb_utils.py", line 193, in _get_pynwb_metadata
    nwb = io.read()
          ^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/pynwb/__init__.py", line 287, in read
    return super().read(**kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/backends/hdf5/h5tools.py", line 453, in read
    return super().read(**kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/backends/io.py", line 42, in read
    container = self.__manager.construct(f_builder)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/manager.py", line 280, in construct
    result = self.__type_map.construct(builder, self, None)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/manager.py", line 789, in construct
    return obj_mapper.construct(builder, build_manager, parent)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 1218, in construct
    subspecs = self.__get_subspec_values(builder, self.spec, manager)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 1147, in __get_subspec_values
    self.__get_sub_builders(groups, spec.groups, manager, ret)
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 1198, in __get_sub_builders
    ret.update(self.__get_subspec_values(sub_builder, subspec, manager))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 1147, in __get_subspec_values
    self.__get_sub_builders(groups, spec.groups, manager, ret)
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 1200, in __get_sub_builders
    ret[subspec] = manager.construct(sub_builder)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/manager.py", line 276, in construct
    result = self.__type_map.construct(builder, self, parent)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/manager.py", line 789, in construct
    return obj_mapper.construct(builder, build_manager, parent)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/utils.py", line 645, in func_call
    return func(args[0], **pargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 1239, in construct
    override = self.__get_override_carg(argname, builder, manager)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/hdmf/build/objectmapper.py", line 524, in __get_override_carg
    return func(self, *remaining_args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/pynwb/io/file.py", line 232, in age_reference_none
    if get_nwb_version(builder) < (2, 6, 0):
       ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/yoh/proj/dandi/dandi-cli-master/venvs/dev3.11/lib/python3.11/site-packages/pynwb/io/utils.py", line 31, in get_nwb_version
    nwb_version_match = re.match(r"(\d+\.\d+\.\d+)", nwb_version)[0]  # trim off any non-numeric symbols at end
                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
```
you can see at the bottom of the traceback -- assumption is that version matches semver but it does not:


❯ python -c 'from dandi.pynwb_utils import get_nwb_version;print(get_nwb_version("/home/yoh/proj/dandi/nwb-datasets/nwb_test_data/v2.0.1/test_Subject.nwb"))'
2.0b
```

below please add 3.11 as a choice of Python version
```


### Operating System

Linux

### Python Executable

Conda

### Python Version

3.10

### Package Versions

_No response_

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/NeurodataWithoutBorders/pynwb/blob/dev/.github/CODE_OF_CONDUCT.rst)
- [X] Have you checked the [Contributing](https://github.com/NeurodataWithoutBorders/pynwb/blob/dev/docs/CONTRIBUTING.rst) document?
- [X] Have you ensured this bug was not already [reported](https://github.com/NeurodataWithoutBorders/pynwb/issues)?
