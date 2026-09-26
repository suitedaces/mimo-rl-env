### Rendering some Jira issue descriptions crashes or produces broken markdown

I'm using jira-cli to view tickets in my terminal (`jira issue view ...`). For most issues this works fine, but a handful of tickets either crash the CLI or render with the entire bottom half of the description swallowed into one giant code block.

After narrowing it down, both cases come from Jira wiki code blocks in the description. I can reproduce by feeding the relevant snippets through `jirawiki.Parse`.

**Case 1 — crash on a code block with a stray colon in the opening tag**

Some tickets in our project have descriptions that look roughly like:

```
{code:}
do_the_thing();
{code}
```

(I've also seen variants where the part after the colon is something the original author probably didn't intend to be parsed as an attribute.)

Running `jira issue view` on these tickets exits immediately with a runtime error instead of printing the ticket — so I can't read the description at all from the CLI.

**Case 2 — closing tag on the same line as content eats the rest of the description**

This one doesn't crash, it just renders wrong. Input:

```
{code}
some line of code
final line of code{code}

Then some more description text below.
Another paragraph.
```

The `{code}` closer is glued to the end of the last code line (this happens a lot when people paste code into Jira's editor and the cursor ends up right before the closer). Expected output is a fenced code block containing the two code lines, followed by the prose below it. What I actually get is a fenced code block that never closes — every line after `{code}` (including the prose paragraphs) becomes part of the code block, and the trailing ``` is misplaced.

Both feel like they should just work — the descriptions render fine in Jira's web UI, and the CLI shouldn't be picky about whether the closing tag has its own line. And it definitely shouldn't crash on an input that Jira itself accepts.
