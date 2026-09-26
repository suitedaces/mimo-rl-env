Tests in koalas currently rely on three different helpers on `ReusedSQLTestCase` for "is this thing equal to that thing?":

- `assert_eq`
- `assert_array_eq`
- `assert_list_eq`

When I'm writing a new test it's not obvious which one to reach for, and I keep guessing wrong — the choice depends on whether the values happen to be a DataFrame/Series, a numpy-style array, or a plain Python list, which often isn't even something I care about at the call site. I just want to say "these two results should match" and let the helper figure out the rest.

It would be much nicer to only have `assert_eq`, and have it handle the cases that `assert_array_eq` / `assert_list_eq` were covering today, so test code doesn't have to pick between three near-duplicates.
