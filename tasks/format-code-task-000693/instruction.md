# Reusable partial conversations via INCLUDE

Our text scripting format lets you write conversations (the `.convo.txt` files) made up of
`#me` / `#bot` steps. As the test suites grow, the same building blocks (logins, greetings,
teardown flows, …) get copy-pasted into many conversations. We want a way to factor those
shared fragments out into reusable pieces and pull them into a conversation on demand.

Please add support for **partial conversations** and an **`INCLUDE` directive**.

## What it should do

- A new script kind, the *partial conversation*, lives in files ending in `.pconvo.txt`. They use
  the exact same text syntax as a normal conversation (a name on the first line, then `#me` /
  `#bot` steps with their asserters/logic hooks). The name of a partial conversation is taken from
  its header (falling back to the file name when no header name is given).
- Partial conversations are **not** runnable conversations on their own: loading a `.pconvo.txt`
  file must not add anything to the regular set of convos. They are kept aside, keyed by name, so
  that other scripts can reference them.
- Inside any conversation step, an `INCLUDE <name>` directive (written like the other logic-hook
  lines, e.g. `PAUSE`) references a partial conversation by name. When that conversation runs, the
  referenced partial conversation's steps are spliced into the conversation in place — i.e. the
  conversation behaves exactly as if the partial conversation's steps had been written inline at
  that point. Both the original and the included steps are executed and appear in the run's
  transcript.
- Includes may be **nested**: a partial conversation can itself `INCLUDE` another one, to arbitrary
  depth, and all of them are expanded.

## Error handling

The following situations must cause a clear failure rather than silently doing the wrong thing:

- **Circular includes.** If expanding the includes would loop back on a partial conversation that
  is already being expanded (directly or transitively), running the conversation must fail with an
  error instead of looping forever.
- **Unknown reference.** If an `INCLUDE` names a partial conversation that does not exist, running
  the conversation must fail with an error.
- **Bad argument.** `INCLUDE` takes exactly one argument (the name). Anything else (zero arguments,
  or more than one) must make the run fail with an error.
- **Duplicate names.** Two partial conversations may not share the same name; loading a second one
  with a name that is already taken must fail with an error.
- **Invalid name.** A partial conversation name may not contain the `|` character; loading one with
  such a name must fail with an error.

Loading the existing `.convo.txt`, `.utterances.txt` and `.xlsx` scripts must keep working exactly
as before.
