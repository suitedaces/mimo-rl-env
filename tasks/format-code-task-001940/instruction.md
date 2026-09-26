Pth file formatting breaks griffe
**Describe the bug**
This pth file https://github.com/mhammond/pywin32/blob/main/pywin32.pth seems to break `_handle_pth_file`. It errors out when checking if the directory exists.

```
  File "...\__pypackages__\3.8\lib\mkdocstrings_handlers\python\handler.py", line 182, in collect
    loader = GriffeLoader(
  File "...\__pypackages__\3.8\lib\griffe\loader.py", line 95, in __init__
    self.finder: ModuleFinder = ModuleFinder(search_paths)
  File "...\__pypackages__\3.8\lib\griffe\finder.py", line 59, in __init__
    self._extend_from_pth_files()
  File "...\__pypackages__\3.8\lib\griffe\finder.py", line 239, in _extend_from_pth_files
    self._append_search_path(_handle_pth_file(item))
  File "...\__pypackages__\3.8\lib\griffe\finder.py", line 282, in _handle_pth_file
    if added_dir.exists():
  File "...\AppData\Local\Programs\Python\Python38\lib\pathlib.py", line 1383, in exists
    self.stat()
  File "...\AppData\Local\Programs\Python\Python38\lib\pathlib.py", line 1189, in stat
    return self._accessor.stat(self)
OSError: [WinError 123] The filename, directory name, or volume label syntax is incorrect: "# .pth file for the PyWin32 extensions\nwin32\nwin32\\lib\nPythonwin\n# And some hackery to deal with environments where the post_install script\n# isn't run.\nimport pywin32_bootstrap"

```

**To Reproduce**
Steps to reproduce the behavior:
1. Install pywin32 package
2. Run griffe through mkdocstrings

mkdocs.yml
```
site_name: "Example"

nav:
- Home: index.md

plugins:
- mkdocstrings:
    default_handler: python

```

index.md
```
::: src.some_file.SomeClass
```

**Expected behavior**
Regardless of whether pywin32 is installed I would expect griffe to run successfully. If I uninstall the package, it works successfully.


**System (please complete the following information):**
- `griffe` version: 0.20.0
- Python version: 3.8
- OS: Windows
