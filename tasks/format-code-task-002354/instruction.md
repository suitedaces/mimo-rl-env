Black fails on docstring with linebreak
<!--
Please make sure that the bug is not already fixed either in newer versions or the
current development version. To confirm this, you have three options:

1. Update Black's version if a newer release exists: `pip install -U black`
2. Use the online formatter at <https://black.vercel.app/?version=main>, which will use
   the latest main branch.
3. Or run _Black_ on your machine:
   - create a new virtualenv (make sure it's the same Python version);
   - clone this repository;
   - run `pip install -e .[d]`;
   - run `pip install -r test_requirements.txt`
   - make sure it's sane by running `python -m pytest`; and
   - run `black` like you did last time.
-->

**Describe the bug**

When you have a docstring and add a \ at the end of the line to get a line break black can't deal with it. 
<!-- A clear and concise description of what the bug is. -->

**To Reproduce**

<!--
Minimal steps to reproduce the behavior with source code and Black's configuration.
-->

For example, take this code:

```python
class Database:
    """
    ## Database Base Class
    The custom ORM specificaly created for the [gitlab-audit project](https://gitlab.itwm.fraunhofer.de/it-linux/gitlab-audit).
    Provides a lot of functions to interact with the database in a pythonic, easy and
    fast way.
    """
    def __init__(self):
        ...
```

It works completely fine(im on python version 3.9.7). But when I now add a \ to get a linebreak it stops working

```python
class Database:
    """
    ## Database Base Class
    The custom ORM specificaly created for the [gitlab-audit project](https://gitlab.itwm.fraunhofer.de/it-linux/gitlab-audit).\ 
    Provides a lot of functions to interact with the database in a pythonic, easy and
    fast way.
    """
    def __init__(self):
        ...
```

The resulting error is:
```sh
error: cannot format /u/f/fuchsf/Documents/gitlab-audit/tools/database_helper.py: INTERNAL ERROR: Black produced code that is not equivalent to the source.  Please report a bug on https://github.com/psf/black/issues.  This diff might be helpful: /var/tmp/blk_jkcx46wd.log
```

Content of /var/tmp/blk_jkcx46wd.log:
```python
--- src
+++ dst
@@ -2569,11 +2569,11 @@
           value=
             Constant(
               kind=
                 None,  # NoneType
               value=
-                '## Database Base Class\nThe custom ORM specificaly created for the [gitlab-audit project](https://gitlab.itwm.fraunhofer.de/it-linux/gitlab-audit).\\\nProvides a lot of functions to interact with the database in a pythonic, easy and\nfast way.',  # str
+                '## Database Base Class\nThe custom ORM specificaly created for the [gitlab-audit project](https://gitlab.itwm.fraunhofer.de/it-linux/gitlab-audit).    Provides a lot of functions to interact with the database in a pythonic, easy and\nfast way.',  # str
             )  # /Constant
         )  # /Expr
         FunctionDef(
           args=
             arguments(

```
**Expected behavior**

<!-- A clear and concise description of what you expected to happen. -->
Black usually shouldn't mess with docstrings since they are not part of the source code. And can sometimes be confusing semi-code. It should just work. 
**Environment**

<!-- Please complete the following information: -->

- Black's version: 23.3.0<!-- e.g. [main] -->
- OS and Python version: Red Hat Linux with Python 3.9.7 in a Virtualenv<!-- e.g. [Linux/Python 3.7.4rc1] -->

**Additional context**

<!-- Add any other context about the problem here. -->
Sadly I can't share anymore code since it's from a closed codebase but if there are any more questions I will try to answer as good as I can
