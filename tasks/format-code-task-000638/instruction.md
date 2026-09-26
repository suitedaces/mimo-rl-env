# Problem Statement

I'm porting the Election contract tests over to Foundry, and I keep needing a few test helpers that don't exist yet in our Solidity test setup. Could we get some shared utilities for things like checking two values are approximately equal (within some margin), comparing whether two address arrays contain the same set, and generating a pseudo-random number in a range for test inputs? Also, I'm trying to read the `DAY`/`WEEK`/`YEAR` constants from a test contract but I can't get at them externally right now — it'd be great if those were reachable from outside.

# Expected outcomes

- Public test constants:
  - `Constants.DAY()`, `Constants.WEEK()`, and `Constants.YEAR()` are readable from outside the contract through the usual Solidity public constant getters.
  - The durations represented by those constants remain unchanged: one day, one week, and one 365-day year respectively.

- Approximate equality helper:
  - `Utils.assertAlmostEqual(uint256 actual, uint256 expected, uint256 margin)` succeeds when `actual` and `expected` differ by no more than `margin`.
  - It fails when the absolute difference is greater than `margin`, and the failure message reports the difference using the `"Difference is "` prefix.

- Address-array set comparison helper:
  - `Utils.arraysEqual(address[] arr1, address[] arr2) -> bool` returns whether the two address arrays represent the same address set.
  - Arrays of different lengths are not considered equal.
  - For arrays of the same length, ordering does not affect equality.

- Pseudo-random test input helper:
  - `Utils.generatePRN(uint256 min, uint256 max, uint256 salt) -> uint256` returns a pseudo-random number suitable for tests.
  - For valid ranges, the returned value is always within the inclusive range `[min, max]`.
  - Across a non-degenerate range, varying the salt should be able to produce varied outputs rather than a fixed boundary or constant value.

# Implementation notes

- These utilities are intended for the Solidity test support layer, not for production contract behavior.
- The concrete data structures, entropy sources, and validation placement are implementation choices, as long as the public helper behavior above is satisfied.
- Existing test utilities should continue to work while the new helpers and externally readable constants are added.
