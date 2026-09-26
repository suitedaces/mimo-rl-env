## Code actions feel stale after I move the cursor, and RuboCop seems to run on every keystroke

I've been using ruby-lsp in VS Code on a moderately sized Ruby file that has several RuboCop offenses spread across the file (say, an indentation issue near the top, a string-quote issue further down, etc.).

### What I'm seeing

When I put my cursor on the first offense and open the lightbulb / quick fix menu, I get the expected fix for that offense. So far so good.

Then I scroll down and click on a *different* offense in another part of the file. I expect the quick fix menu to show me an action for *this* offense. Instead I keep getting the same code action I got the first time, as if the editor is still showing me suggestions for the previous cursor location. If I keep moving around, the suggestions don't seem to track where I actually am in the file — they look frozen on whatever range was used the first time `textDocument/codeAction` fired for this file.

### And separately (but I suspect related)

While poking at this, I noticed the editor stalls noticeably every time code actions get requested, even when I haven't edited the file at all between requests — just moved the cursor. Watching activity, it looks like RuboCop is being re-run from scratch over and over for the same unchanged file contents. For a file that hasn't changed, re-analyzing it every time the cursor moves feels wrong and is making the experience pretty laggy.

### What I'd expect

- Code actions should reflect the current selection / visible range. Moving my cursor to a different offense should give me the fix for *that* offense, not a cached one from earlier.
- Re-analyzing the file with RuboCop when nothing about the file has changed seems wasteful — that part I'd expect to be reused across requests on the same unchanged document.

Right now it feels like the two are inverted: the thing that depends on where I'm looking is sticky, and the thing that doesn't depend on where I'm looking is being recomputed every time.
