# Problem Statement

When I submit a rule with a bad SQL statement, the validation errors are pretty useless — I just get something like "Not allowed to call aggregate functions in WHERE clause" or "validate function arguments failed" with no clue which part of my query actually broke. With several clauses and functions in play, I'm left guessing where the problem is. Could the error messages point to the specific clause or function that failed? Just having it include the offending expression or function name would save me a ton of trial and error.

# Expected outcomes

- SQL validation errors caused by a specific clause expression should include enough of that offending expression to let the user identify which part of the query failed, instead of returning only a generic clause-level message.
- Function-related validation errors should identify the relevant function whose arguments failed validation and, when there is a more specific underlying validation reason, preserve that reason in the reported error.

# Implementation notes

- Preserve the existing validation semantics: invalid queries and invalid function calls should still fail, while valid ones should continue to pass.
- The exact code organization, validation layer, and formatting mechanism are implementation choices, as long as the user-visible error messages include the relevant clause expression or function name and retain the underlying reason where applicable.
