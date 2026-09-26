mypy 0.670 crashes with AssertionError: Var is lacking info
Note: if you are reporting a wrong signature of a function or a class in
the standard library, then the typeshed tracker is better suited
for this report: https://github.com/python/typeshed/issues

Please provide more information to help us understand the issue:

* Are you reporting a bug, or opening a feature request? **Bug**
* Please insert below the code you are checking with mypy,
  or a mock-up repro if the source is private. We would appreciate
  if you try to simplify your case to a minimal repro.
* What is the actual behavior/output? **Crash with INTERNAL ERROR**
* What is the behavior/output you expect? **No crash**
* What are the versions of mypy and Python you are using?
  Do you see the same issue after installing mypy from Git master? **0.670, haven't had time to try out master**
* What are the mypy flags you are using? (For example --strict-optional) **No flags**
* If mypy crashed with a traceback, please paste
  the full traceback below.

Context: the below code works fine if replacing `self.dill` with `Test.dill` since it is a class variable. This also causes mypy to not crash.

### Code:
```python
class Test:
    import dill
    def __init__(self) -> None:
        some_module = self.dill
```

### Traceback:
```
test.py:4: error: Cannot find module named 'dill'
test.py:4: note: See https://mypy.readthedocs.io/en/latest/running_mypy.html#missing-imports
test.py:13: error: INTERNAL ERROR -- please report a bug at https://github.com/python/mypy/issues version: 0.670
Traceback (most recent call last):
  File "c:\miniconda3\envs\refactoring\lib\runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "c:\miniconda3\envs\refactoring\lib\runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "C:\Miniconda3\envs\refactoring\Scripts\mypy.exe\__main__.py", line 9, in <module>
    sys.exit(console_entry())
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\__main__.py", line 7, in console_entry
    main(None)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\main.py", line 91, in main
    res = build.build(sources, options, None, flush_errors, fscache)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\build.py", line 162, in build
    result = _build(sources, options, alt_lib_path, flush_errors, fscache)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\build.py", line 217, in _build
    graph = dispatch(sources, manager)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\build.py", line 2360, in dispatch
    process_graph(graph, manager)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\build.py", line 2660, in process_graph
    process_stale_scc(graph, scc, manager)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\build.py", line 2767, in process_stale_scc
    graph[id].type_check_first_pass()
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\build.py", line 1919, in type_check_first_pass
    self.type_checker().check_first_pass()
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 282, in check_first_pass
    self.accept(d)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 846, in accept
    return visitor.visit_class_def(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1537, in visit_class_def
    self.accept(defn.defs)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 911, in accept
    return visitor.visit_block(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1701, in visit_block
    self.accept(s)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 606, in accept
    return visitor.visit_func_def(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 704, in visit_func_def
    self._visit_func_def(defn)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 708, in _visit_func_def
    self.check_func_item(defn, name=defn.name())
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 770, in check_func_item
    self.check_func_def(defn, typ, name)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 932, in check_func_def
    self.accept(item.body)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 911, in accept
    return visitor.visit_block(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1701, in visit_block
    self.accept(s)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 1102, in accept
    return visitor.visit_if_stmt(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 2734, in visit_if_stmt
    self.accept(b)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 911, in accept
    return visitor.visit_block(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1701, in visit_block
    self.accept(s)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 1102, in accept
    return visitor.visit_if_stmt(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 2734, in visit_if_stmt
    self.accept(b)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 911, in accept
    return visitor.visit_block(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1701, in visit_block
    self.accept(s)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 393, in accept
    stmt.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 969, in accept
    return visitor.visit_assignment_stmt(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1709, in visit_assignment_stmt
    self.check_assignment(s.lvalues[-1], s.rvalue, s.type is None, s.new_syntax)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checker.py", line 1828, in check_assignment
    in_final_declaration=inferred.is_final,
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkexpr.py", line 3188, in accept
    typ = node.accept(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 1398, in accept
    return visitor.visit_member_expr(self)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkexpr.py", line 1761, in visit_member_expr
    result = self.analyze_ordinary_member_access(e, is_lvalue)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkexpr.py", line 1776, in analyze_ordinary_member_access
    in_literal_context=self.is_literal_context())
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkmember.py", line 101, in analyze_member_access
    result = _analyze_member_access(name, typ, mx, override_info)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkmember.py", line 115, in _analyze_member_access
    return analyze_instance_member_access(name, typ, mx, override_info)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkmember.py", line 188, in analyze_instance_member_access
    return analyze_member_var_access(name, typ, info, mx)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkmember.py", line 327, in analyze_member_var_access
    return analyze_var(name, v, itype, info, mx, implicit=implicit)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\checkmember.py", line 470, in analyze_var
    itype = map_instance_to_supertype(itype, var.info)
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\maptype.py", line 20, in map_instance_to_supertype
    if not superclass.type_vars:
  File "c:\miniconda3\envs\refactoring\lib\site-packages\mypy\nodes.py", line 2525, in __getattribute__
    raise AssertionError(object.__getattribute__(self, 'msg'))
AssertionError: Var is lacking info
test.py:13: : note: use --pdb to drop into pdb
```
