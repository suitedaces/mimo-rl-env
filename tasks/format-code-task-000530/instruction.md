sort-* function fails on empty seq
Hi,

sort-* functions return an error on empty seq
```TypeError: 'NoneType' object is not iterable```

To reproduce.
1. Open up a REPL and try to sort an empty seq
``` clojure
basilisp.user=> (sort (seq []))
Traceback (most recent call last):
  File "C:\src\basilisp\src\basilisp\cli.py", line 306, in repl
    result = eval_str(lsrc, ctx, ns, eof)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\src\basilisp\src\basilisp\cli.py", line 52, in eval_str
    last = compiler.compile_and_exec_form(form, ctx, ns)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\src\basilisp\src\basilisp\lang\compiler\__init__.py", line 165, in compile_and_exec_form
    return getattr(ns.module, final_wrapped_name)()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<REPL Input>", line 1, in __lisp_expr___65
  File "C:\src\basilisp\src\basilisp\core.lpy", line 1160, in sort
    (defn sort
  File "C:\src\basilisp\src\basilisp\core.lpy", line 1165, in sort__arity1
    (basilisp.lang.runtime/sort coll))
  File "C:\src\basilisp\src\basilisp\lang\runtime.py", line 1432, in sort
    return lseq.sequence(sorted(coll, key=key))
                         ^^^^^^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not iterable
```

Clojure returns an empty seq instead
``` clojure
user> (sort (seq []))
()
```

PR to follow.
