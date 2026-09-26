Classifiers: Python version sort order
<!--
    NOTE: This issue should be for problems with PyPI itself, including:
    * pypi.org
    * test.pypi.org
    * files.pythonhosted.org

    This issue should NOT be for a project installed from PyPI. If you are
    having an issue with a specific package, you should reach out to the
    maintainers of that project directly instead.

    Furthermore, this issue should NOT be for any non-PyPI properties (like
    python.org, docs.python.org, etc.)
-->

**Describe the bug**
<!-- A clear and concise description the bug -->

The classifiers "Programming Language :: Python :: 3.X" aren't sorted in the right order on https://pypi.org as well as on https://test.pypi.org

I'm defining the classifiers like this in the `setup.py` file.

```
classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10"
    ]
```

In the navigation bar on pypy.org it will then appear like this: 
![image](https://user-images.githubusercontent.com/70264417/99465712-42797f00-293b-11eb-8f1a-dced842f433f.png)

With Python 3.10 at the top instead of at the bottom (after Python 3.9).


To give the visitors of pypi.org a better and faster overview over a project, it would be great if the Python classifiers were sorted by the Python versions.


**Expected behavior**
<!-- A clear and concise description of what you expected to happen -->

Classifiers sorted by Python versions.

Python :: 3
Python :: 3.6
Python :: 3.7
Python :: 3.8
Python :: 3.9
Python :: 3.10
Python :: 3.11
Python :: 3.12
etc.

**To Reproduce**
<!-- Steps to reproduce the bug, or a link to PyPI where the bug is visible -->

It can be seen for example here: https://pypi.org/project/officeextractor/
