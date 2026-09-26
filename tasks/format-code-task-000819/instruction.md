## `added_on` gets reset after running `dnote sync`

I noticed that the creation time of my notes is being clobbered by `dnote sync`.

Repro:

1. `dnote add somebook` — write a quick note. At this point looking at the note locally shows the correct `added_on` (the time I created it).
2. `dnote sync`
3. Inspect the same note again.

After step 3 the `added_on` value is no longer the time I created the note — it looks like it got wiped to a zero / epoch-ish value. The note body, book and other fields look fine; only the creation timestamp is wrong.

`added_on` is supposed to be set once when the note is first created and stay that way. Sync shouldn't be touching it. Right now every time I sync, any newly-created (still-dirty) note loses its real creation time.

Could you take a look? Happy to provide more details if needed.
