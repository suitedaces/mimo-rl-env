### `--target-version` involving Python 2 picks the wrong grammar

I maintain a library that still supports Python 2.7 alongside Python 3, and I was excited to try Black's `--target-version` flag to lock the formatting to my supported versions. While experimenting I noticed the grammar selection doesn't seem to respect what I pass in.

A couple of cases that look wrong to me:

1. **Mixed targets behave like pure Python 2.** If I pass `--target-version py27 --target-version py36`, code that I *know* is fine as Py3 (e.g. `exec(code, ns)` used as a regular function call) gets reformatted in ways that only make sense if Black is parsing it under a Python 2 grammar where `exec` is still a statement. Since the code has to be valid under *every* target I list, I'd expect the stricter (Py3) grammar to win in a mixed configuration.

2. **Pure Python 3 target still falls back to Py2-ish grammars.** Even with just `--target-version py36`, I can construct snippets that get parsed as if `exec` / `print` were statements when they shouldn't be — I explicitly told Black this is Python 3 code, so it shouldn't even be considering those grammars.

3. Conversely, when I pass `--target-version py27` on truly Python-2-only code (with `print` statements, `exec` statements, etc.), I'd expect Black to commit to the Python 2 grammars and not waste time / risk misparsing under a Py3 grammar.

In short: when I specify target versions explicitly, the choice of grammars Black tries should match what I asked for. Today the behavior seems to be driven by "is there *any* non-Py2 version in the set" rather than "is the code required to be Py3-compatible", and the two are not the same thing.

The autodetect path (no `--target-version` given) seems fine — it's only when I'm explicit about targets that things go sideways. Could you take a look at how target versions map to the grammars Black attempts?
