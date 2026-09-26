BUG: Wrong Latex Encoding
Assume a ``DataFrame`` ``df`` that looks like this:


    |      A      | B | ... |
    -------------------------
    |    a\b\c    | 2 | ... |
    |    p\y\c    | 9 | ... |
    |    a\d\x    | 4 | ... |

Calling ``to_latex`` on this ``DataFrame`` returns strings like ``a\textbackslashb\textbackslashc``, what obviously is an error for LaTeX. Expected and correct is  ``a\textbackslash b\textbackslash c``.

Tried with current master ``0.23.0.dev0+808.gd92d76e.dirty`` as well as with release ``0.22.0``.

Using ``escape=False`` returns ``a\b\c`` what is also an error for LaTeX (but expected). 
So there is no way currently to get valid LaTeX code from a DataFrame like this.
