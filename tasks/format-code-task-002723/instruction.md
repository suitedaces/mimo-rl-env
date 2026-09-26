LT02 ValueError: max() arg is an empty sequence (Jinja templater)
### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

Crash in LT02

### Expected Behaviour

No crash.

### Observed Behaviour

```
CRITICAL   [LT02] Applying rule LT02 to 'repro.sql' threw an Exception: max() arg is an empty sequence                                                                                                                       
Traceback (most recent call last):
  File "/home/lrogalski/<redacted>/.venv/lib/python3.11/site-packages/sqlfluff/core/rules/base.py", line 511, in crawl
    res = self._eval(context=context)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lrogalski/<redacted>/.venv/lib/python3.11/site-packages/sqlfluff/rules/layout/LT02.py", line 64, in _eval
    .reindent()
     ^^^^^^^^^^
  File "/home/lrogalski/<redacted>/.venv/lib/python3.11/site-packages/sqlfluff/utils/reflow/sequence.py", line 578, in reindent
    elements, indent_results = lint_indent_points(
                               ^^^^^^^^^^^^^^^^^^^
  File "/home/lrogalski/<redacted>/.venv/lib/python3.11/site-packages/sqlfluff/utils/reflow/reindent.py", line 1658, in lint_indent_points
    _revise_templated_lines(lines, elements)
  File "/home/lrogalski/<redacted>/.venv/lib/python3.11/site-packages/sqlfluff/utils/reflow/reindent.py", line 584, in _revise_templated_lines
    best_indent = max(overlap)
                  ^^^^^^^^^^^^
ValueError: max() arg is an empty sequence
== [repro.sql] FAIL                                                                                                                                                                                                          
L:   1 | P:   1 | LT02 | Unexpected exception: max() arg is an empty
                       | sequence;
Could you open an issue at
                       | https://github.com/sqlfluff/sqlfluff/issues ?
You can
                       | ignore this exception for now, by adding '-- noqa: LT02'
                       | at the end
of line 1
 [layout.indent]

```

### How to reproduce

```sql
-- sqlfluff:templater:jinja:context:tables:['tbl_a','tbl_b','tbl_c']
-- sqlfluff:templater:jinja:context:each_table_cols:[['aa', 'ab', 'ac'],['ba','bb','bc'],['ca','cb','cc']]
-- sqlfluff:indentation:template_blocks_indent:false

CREATE OR REPLACE TRANSIENT TABLE TEST AS
WITH abc AS (
    SELECT
        spine.some_id AS some_id
        {% for cols in each_table_cols -%}
        {%- set src_loop = loop -%}
        {%- for c in cols -%}
        , t{{ src_loop.index }}."{{ c }}"
        {% endfor %}
        {%- endfor %}
    FROM tbl AS spine
    {% for t in tables %}
    LEFT JOIN {{ t }} AS t{{ loop.index }}
    ON spine.some_id = t{{ loop.index }}.some_id
    {% endfor %}
)

SELECT * FROM abc;
```

Rendered looks quite good:
```sql
-- sqlfluff:templater:jinja:context:tables:['tbl_a','tbl_b','tbl_c']
-- sqlfluff:templater:jinja:context:each_table_cols:[['aa', 'ab', 'ac'],['ba','bb','bc'],['ca','cb','cc']]
-- sqlfluff:indentation:template_blocks_indent:false

CREATE OR REPLACE TRANSIENT TABLE TEST AS
WITH abc AS (
    SELECT
        spine.some_id AS some_id
        , t1."aa"
        , t1."ab"
        , t1."ac"
        , t2."ba"
        , t2."bb"
        , t2."bc"
        , t3."ca"
        , t3."cb"
        , t3."cc"

    FROM tbl AS spine

    LEFT JOIN tbl_a AS t1
    ON spine.some_id = t1.some_id

    LEFT JOIN tbl_b AS t2
    ON spine.some_id = t2.some_id

    LEFT JOIN tbl_c AS t3
    ON spine.some_id = t3.some_id

)

SELECT * FROM abc;
```

### Dialect

ansi

### Version

No crash in 3.2.2.
Crash in 3.2.3. 

### Configuration

inlined

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
