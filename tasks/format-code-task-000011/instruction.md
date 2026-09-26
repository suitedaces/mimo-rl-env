## 1277 and 338 directories are placeholders — please fill them in

I was browsing this repo looking for the Go solutions to a couple of LeetCode problems and noticed that **1277. Count Square Submatrices with All Ones** and **338. Counting Bits** both appear to be unfinished placeholders.

In `leetcode/1201-1300/1277.Count-Square-Submatrices-with-All-Ones/` and `leetcode/301-400/0338.Counting-Bits/`, the contents look like this:

- `README.md` has the `> [!WARNING|style:flat]` banner saying *"This question is temporarily unanswered if you have good ideas. Welcome to Create Pull Request PR"*.
- The `## Description` section is mostly empty, and the only example given is:
  ```
  Input: a = "11", b = "1"
  Output: "100"
  ```
  which clearly belongs to some other problem (looks like a string-addition / add-binary kind of question), not to 1277 or 338.
- `Solution.go` only contains the dummy stub:
  ```go
  package Solution

  func Solution(x bool) bool {
      return x
  }
  ```
  The `bool` signature obviously doesn't match either problem — 1277 takes a 2D matrix and returns a count, 338 takes an integer `n` and returns a slice.

Could someone fill these two in properly? Specifically, for each of the two problems:

- update `README.md` so the description and example(s) actually match what LeetCode is asking for,
- and replace the stub `Solution.go` with a real implementation using a function signature that fits the problem's input/output.

Happy to review if someone picks them up. Thanks!
