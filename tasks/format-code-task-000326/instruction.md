# Support formatted poll questions and answer options

Telegram now lets bots send polls whose **question** and **answer options** carry text
formatting (bold, italic, custom emoji, …). Right now our `send_poll` support is stuck on the
old shape: answer options are plain strings only, and there's no way to format the question.
Let's bring the poll API up to date.

## What we need

**A new input type for answer options.** Introduce a public type that represents a single answer
option to be sent (not the one returned in poll results). It must be importable from the
top-level types package and carry:

- `text` — the option text (required).
- `text_parse_mode` — optional parse mode for the option text.
- `text_entities` — an optional list of message entities for the option text. When constructed
  from raw data (e.g. a list of dicts), these must be parsed into the usual message-entity
  objects, like every other entities field in the library.

Only the fields actually provided should appear when the object is serialized (no spurious
`null`s for the optional fields).

**`send_poll` should accept formatted options.** The `options` argument must accept a list whose
items are *either* plain strings *or* the new input-option objects, freely mixed in the same
list. Plain strings must stay plain strings, and option objects must be preserved as-is — passing
an option object where only a string used to be allowed must now work.

**`send_poll` should accept a formatted question.** Add two new parameters:

- `question_parse_mode` — parse mode for the poll question. Like the explanation parse mode, it
  should fall back to the bot's default parse mode when not given explicitly.
- `question_entities` — an optional list of message entities for the question, usable instead of
  `question_parse_mode`. These must be parsed into message-entity objects.

Both must be real parameters of the method (and of the corresponding `Bot.send_poll` helper), not
just arbitrary extra keyword arguments.

**Returned poll data should expose the new entities.** The poll object returned by Telegram now
includes formatting entities for the question, and each answer option in poll results now includes
formatting entities for its text. Add the corresponding optional fields so that:

- the poll object gains a `question_entities` list, and
- the answer-option result object gains a `text_entities` list,

both parsed into message-entity objects when present.

Existing call sites that pass `options=["A", "B"]` and never touch the new fields must keep working
exactly as before.
