**Parameterized test names containing `[` or `]` render incorrectly**

Hi! I've been trying out `com.adarshr.test-logger` on a project that has a bunch of Spock `@Unroll` parameterized tests, and the rendered output looks broken whenever a test name contains square brackets.

Spock expands `@Unroll`'d feature methods into names that include the iteration's data values inside `[ ... ]`, e.g.:

```
my feature method [a=1, b=2]
```

When test-logger prints those lines to the terminal, the line gets mangled starting from the first `[` — characters disappear and/or the styling/colour on the rest of that line is off compared to a non-parameterized test on the same run. JUnit's parameterized runner has the same problem since it produces names like `myTest[0]` or `myTest[someValue]`.

I tried switching themes (default and mocha) and the breakage is present in both, so it doesn't look like a theme-specific quirk.

I'd expect the test name to be printed verbatim regardless of which characters it happens to contain — `[` and `]` shouldn't be treated as anything special when they originate from the test descriptor. This is fairly important for any project that uses parameterized tests, because right now those rows are basically unreadable.
