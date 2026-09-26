Passing dataclass `default_factory` as positional argument causes internal error.
<!--
  Use this form only if mypy reports an "INTERNAL ERROR" and/or gives a traceback.
  Please include the traceback and all other messages below (use `mypy --show-traceback`).
-->

**Crash Report**

The detaclasses ``field`` is missing a ``default_factory`` keyword argument. I'm passing it as a positional argument.

**Traceback**

```
Traceback (most recent call last):
  File "/home/jonathan/.pyenv/versions/lazy-maestro-3.9/bin/mypy", line 33, in <module>
    sys.exit(load_entry_point('mypy', 'console_scripts', 'mypy')())
  File "/home/jonathan/git/mypy/mypy/__main__.py", line 11, in console_entry
    main(None, sys.stdout, sys.stderr)
  File "/home/jonathan/git/mypy/mypy/main.py", line 98, in main
    res = build.build(sources, options, None, flush_errors, fscache, stdout, stderr)
  File "/home/jonathan/git/mypy/mypy/build.py", line 179, in build
    result = _build(
  File "/home/jonathan/git/mypy/mypy/build.py", line 253, in _build
    graph = dispatch(sources, manager, stdout)
  File "/home/jonathan/git/mypy/mypy/build.py", line 2688, in dispatch
    process_graph(graph, manager)
  File "/home/jonathan/git/mypy/mypy/build.py", line 3012, in process_graph
    process_stale_scc(graph, scc, manager)
  File "/home/jonathan/git/mypy/mypy/build.py", line 3104, in process_stale_scc
    mypy.semanal_main.semantic_analysis_for_scc(graph, scc, manager.errors)
  File "/home/jonathan/git/mypy/mypy/semanal_main.py", line 78, in semantic_analysis_for_scc
    process_top_levels(graph, scc, patches)
  File "/home/jonathan/git/mypy/mypy/semanal_main.py", line 199, in process_top_levels
    deferred, incomplete, progress = semantic_analyze_target(next_id, state,
  File "/home/jonathan/git/mypy/mypy/semanal_main.py", line 326, in semantic_analyze_target
    analyzer.refresh_partial(refresh_node,
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 394, in refresh_partial
    self.refresh_top_level(node)
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 405, in refresh_top_level
    self.accept(d)
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 4835, in accept
    node.accept(self)
  File "/home/jonathan/git/mypy/mypy/nodes.py", line 950, in accept
    return visitor.visit_class_def(self)
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 1048, in visit_class_def
    self.analyze_class(defn)
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 1125, in analyze_class
    self.analyze_class_body_common(defn)
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 1134, in analyze_class_body_common
    self.apply_class_plugin_hooks(defn)
  File "/home/jonathan/git/mypy/mypy/semanal.py", line 1180, in apply_class_plugin_hooks
    hook(ClassDefContext(defn, decorator, self))
  File "/home/jonathan/git/mypy/mypy/plugins/dataclasses.py", line 361, in dataclass_class_maker_callback
    transformer.transform()
  File "/home/jonathan/git/mypy/mypy/plugins/dataclasses.py", line 100, in transform
    attributes = self.collect_attributes()
  File "/home/jonathan/git/mypy/mypy/plugins/dataclasses.py", line 249, in collect_attributes
    has_field_call, field_args = _collect_field_args(stmt.rvalue)
  File "/home/jonathan/git/mypy/mypy/plugins/dataclasses.py", line 378, in _collect_field_args
    assert name is not None.)
```

**To Reproduce**

```python
from dataclasses import dataclass, field

@dataclass
class C:
    attribute: int = field(int)
```

**Your Environment**

<!-- Include as many relevant details about the environment you experienced the bug in -->

- Mypy version used: mypy 0.820+dev.797544d8f97c478770eb178ba966cc7b1d0e6020.dirty
- Mypy command-line flags: none
- Mypy configuration options from `mypy.ini` (and other config files): /
- Python version used: 3.9.2
- Operating system and version: Linux
