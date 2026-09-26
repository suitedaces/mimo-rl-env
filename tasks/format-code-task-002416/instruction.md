Extracted method fails when it contains multi subscriptables
**Describe the bug**

Error while extracting method that contains augmented assignment to multi subscriptables (dict, list etc.).

**To Reproduce**

Steps to reproduce the behavior:

1. Code before refactoring:

```
def my_method():
    my_var = [[0], [1], [2]]
    my_var[0][0] += 1
    print(1)
```

2. Describe the refactoring you want to do

Select the `print(1)` line, and then trigger `Extract method`.

3. Expected code after refactoring:

```
def my_method():
    my_var = [[0], [1], [2]]
    my_var[0][0] += 1
    extracted_method()

def extracted_method():
    print(1)
```

4. Describe the error or unexpected result that you are getting

Exception occured and code didn't change.

```
Traceback (most recent call last):
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/pylsp_rope/plugin.py", line 152, in pylsp_execute_command
    return commands[command](workspace, **arguments[0])()
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/pylsp_rope/plugin.py", line 176, in __call__
    rope_changeset = self.get_changes()
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/pylsp_rope/plugin.py", line 240, in get_changes
    rope_changeset = refactoring.get_changes(
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 83, in get_changes
    new_contents = _ExtractPerformer(info).extract()
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 274, in extract
    extract_info = self._collect_info()
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 300, in _collect_info
    self._find_definition(extract_collector)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 372, in _find_definition
    parts = _ExtractMethodParts(self.info)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 507, in __init__
    self.info_collector = self._create_info_collector()
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 579, in _create_info_collector
    ast.walk(node, info_collector)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/base/ast.py", line 41, in walk
    walk(child, walker)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/base/ast.py", line 39, in walk
    return method(node)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 813, in _FunctionDef
    ast.walk(child, self)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/base/ast.py", line 39, in walk
    return method(node)
  File "/home/naokisz/python/rope_issue/__pypackages__/3.10/lib/rope/refactor/extract.py", line 847, in _AugAssign
    target_id = node.target.value.id
AttributeError: 'Subscript' object has no attribute 'id'
```

**Editor information (please complete the following information):**
 - Project Python version: python 3.10.7
 - Rope Python version: python 3.10.7
 - Rope version: rope 1.3.0
 - Text editor/IDE and version: Neovim with pylsp-rope 0.1.10

**Additional context**

This issue may be related to #459 because same exception occured.  
But this issue differs from #459 in that #459 doesn't contain multi subscriptables and contains try..except block.
