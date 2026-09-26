## Feature request: E-Prime check

I write a fair amount of technical prose in [E-Prime](https://en.wikipedia.org/wiki/E-Prime) style, which means avoiding all forms of the verb "to be" (is, was, been, etc.). I'd love to use `write-good` as part of my workflow to flag those verbs, but looking at the current list of checks (`passive`, `weasel`, `cliches`, etc.) there's nothing that catches "to be" forms specifically — passive voice catches some of them but misses plenty (e.g. "The sky is blue.").

Would you consider adding an E-Prime check to write-good?

One thing to keep in mind: most users probably *don't* write in E-Prime, and flagging every "is/was/are" by default would be incredibly noisy and almost certainly unwanted. So this check should be off by default, and only run when the user explicitly asks for it — both from the JS API (passing it in `opts`) and from the CLI.

The current CLI only seems to support turning checks *off* (`--no-passive`); there's no obvious way to opt *into* a check that ships disabled by default. So enabling an opt-in check from the command line would need some thought too.

Programmatic usage I'd expect to look something like:

```js
var writeGood = require('write-good');
// default — no E-Prime noise
writeGood('The sky is blue.'); // []

// opt in
writeGood('The sky is blue.', { /* enable eprime */ });
// -> suggestion flagging "is"
```

Happy to help review if someone wants to take a stab at it.
