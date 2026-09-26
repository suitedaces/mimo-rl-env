bug: relocate not working as expected
### What happened?

setup code -- load the penguins table on Ibis installed on master:

```python
[ins] In [1]: import ibis
[ins] In [2]: import ibis.selectors as s
[ins] In [3]: ibis.options.interactive = True
[ins] In [4]: ibis.options.repr.interactive.max_rows = 3
[ins] In [5]: t = ibis.examples.penguins.fetch()

[ins] In [6]: t
Out[6]:
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ species ┃ island    ┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ sex    ┃ year  ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ string  │ string    │ float64        │ float64       │ int64             │ int64       │ string │ int64 │
├─────────┼───────────┼────────────────┼───────────────┼───────────────────┼─────────────┼────────┼───────┤
│ Adelie  │ Torgersen │           39.1 │          18.7 │               181 │        3750 │ male   │  2007 │
│ Adelie  │ Torgersen │           39.5 │          17.4 │               186 │        3800 │ female │  2007 │
│ Adelie  │ Torgersen │           40.3 │          18.0 │               195 │        3250 │ female │  2007 │
│ …       │ …         │              … │             … │                 … │           … │ …      │     … │
└─────────┴───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┴───────┘
```

I would expect this to put "year", followed by numeric columns -- instead, numeric columns are first:

```python
[ins] In [7]: t.relocate("year", s.numeric())
Out[7]:
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┓
┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ year  ┃ species ┃ island    ┃ sex    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━┩
│ float64        │ float64       │ int64             │ int64       │ int64 │ string  │ string    │ string │
├────────────────┼───────────────┼───────────────────┼─────────────┼───────┼─────────┼───────────┼────────┤
│           39.1 │          18.7 │               181 │        3750 │  2007 │ Adelie  │ Torgersen │ male   │
│           39.5 │          17.4 │               186 │        3800 │  2007 │ Adelie  │ Torgersen │ female │
│           40.3 │          18.0 │               195 │        3250 │  2007 │ Adelie  │ Torgersen │ female │
│              … │             … │                 … │           … │     … │ …       │ …         │ …      │
└────────────────┴───────────────┴───────────────────┴─────────────┴───────┴─────────┴───────────┴────────┘
```

I would then expect this to do the opposite:

```python
[nav] In [8]: t.relocate(s.numeric(), "year")
Out[8]:
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┓
┃ bill_length_mm ┃ bill_depth_mm ┃ flipper_length_mm ┃ body_mass_g ┃ year  ┃ species ┃ island    ┃ sex    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━┩
│ float64        │ float64       │ int64             │ int64       │ int64 │ string  │ string    │ string │
├────────────────┼───────────────┼───────────────────┼─────────────┼───────┼─────────┼───────────┼────────┤
│           39.1 │          18.7 │               181 │        3750 │  2007 │ Adelie  │ Torgersen │ male   │
│           39.5 │          17.4 │               186 │        3800 │  2007 │ Adelie  │ Torgersen │ female │
│           40.3 │          18.0 │               195 │        3250 │  2007 │ Adelie  │ Torgersen │ female │
│              … │             … │                 … │           … │     … │ …       │ …         │ …      │
└────────────────┴───────────────┴───────────────────┴─────────────┴───────┴─────────┴───────────┴────────┘
```

### What version of ibis are you using?

master

### What backend(s) are you using, if any?

duckdb

### Relevant log output

```sh
n/a, see above
```


### Code of Conduct

- [X] I agree to follow this project's Code of Conduct
