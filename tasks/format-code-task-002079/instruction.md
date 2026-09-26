## Recent change to NaT comparisons broke a lot of existing code

I updated to a recent dev build of numpy and a bunch of code that was working fine on 1.10 started failing. After narrowing it down, it looks like the comparison semantics for `datetime64('NaT')` / `timedelta64('NaT')` changed.

Two concrete things I hit:

**1. The usual idiom for filtering out NaT no longer works.**

I have timedelta64 arrays that may contain NaT, and I've been using

```python
clean = arr[arr == arr]
```

to drop the NaT entries (same trick people use for NaN floats — only it relied on NaT *not* behaving like NaN here). On the new build this returns an empty array even when there are perfectly good non-NaT values in `arr`, because `NaT == NaT` is now False. A bunch of formatting / summary code I have on top of timedelta arrays silently breaks because of this.

**2. Direct equality between two NaT values flipped.**

```python
nat = np.datetime64('NaT')
nat == nat   # used to be True, now False
nat != nat   # used to be False, now True
```

This breaks straightforward equality checks and assertions in downstream code. Pandas in particular has a lot of tests that assume NaT compares equal to itself, and they're now failing against numpy master.

I get the appeal of making NaT behave like NaN (propagating "missing" through comparisons), and maybe that's the right long-term direction. But flipping it in one release with no warning has too much downstream fallout — pandas tests are red, and any user code that used `arr[arr == arr]` to strip NaT will silently start producing wrong results without any error.

Could we put NaT comparison back to the previous behavior (NaT equal to itself, the filtering idiom keeps working) for now, and stage the NaN-style change properly via a deprecation / FutureWarning over a couple of releases before actually flipping it? The current state is too breaking to ship as-is.
