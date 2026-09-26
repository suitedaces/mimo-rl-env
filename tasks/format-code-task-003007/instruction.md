## Library improvements for downstream integrations

I'm integrating `sucks` into Home Assistant and ran into a few rough edges while wrapping `VacBot` for end users. None of these are bugs — the library works — but they each push complexity onto the integrator that I think really belongs in the library itself.

### 1. No high-level "is the vacuum cleaning / charging?" check

In my integration I want to show the user a simple "currently cleaning" indicator. Today, `VacBot` only exposes the raw `vacuum_status` / `clean_status` / `charge_status` strings, so I end up doing something like:

```python
if vacbot.vacuum_status in (some, set, of, strings, I, had, to, figure, out):
    cleaning = True
```

To build that set correctly I had to read the source and figure out which status values actually represent active cleaning vs. just "stopped", "returning", "charging", etc. That mapping is really library knowledge — every downstream consumer is going to re-derive (and probably get wrong) the same answer. And if `sucks` ever adds or renames a cleaning mode, every integration silently breaks until each maintainer updates their own copy of that set.

Same story for "is the vacuum currently charging?". It would be much nicer if `VacBot` itself answered these two questions and owned the definition of what counts.

### 2. Status / mode / component strings aren't importable as constants

Related to the above: when I want to compare against a specific status (e.g. to react when the bot enters a particular mode, or to drive a state machine in my integration), I have to hard-code string literals like `'auto'`, `'charging'`, `'main_brush'`, etc. directly in my code. These strings live inside dictionaries in `sucks/__init__.py` but aren't exposed as named values I can `from sucks import ...`.

This means:
- My integration is full of magic strings that aren't checked anywhere — a typo just silently fails to match.
- If `sucks` ever decides to rename one of these (say, a cleaning mode), every consumer has to chase the change manually instead of just picking up a new library version.

Could the vocabulary the library uses for clean modes, fan speeds, charge modes, and components be exposed as named constants that consumers are expected to import and use, instead of being implicit in the dict values?

### 3. Logging goes to the root logger, not a `sucks`-scoped one

The library currently calls `logging.debug(...)` / `logging.warning(...)` etc. directly, which routes everything through the root logger. In Home Assistant, users configure log levels per integration/library via YAML, e.g. to crank `sucks` up to DEBUG while leaving everything else at WARNING. That only works if the library logs through a logger named after its module (the standard `logging.getLogger(__name__)` pattern from the Python docs).

Right now there's no way for an HA user to enable verbose `sucks` logging without also turning up the volume on every other library in the process, which is pretty unfriendly for debugging vacuum issues in the field.

---

All three of these are pretty mechanical changes but they'd make `sucks` noticeably nicer to build on top of. Happy to help if useful.

For the first item, I'd expect the API on `VacBot` to look something like `is_cleaning` / `is_charging` (boolean properties).
