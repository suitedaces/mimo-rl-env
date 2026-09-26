## `SymfonyStyle::ask()` doesn't render inline formatting tags in the question text

I'm writing an interactive command and wanted to highlight a word inside the prompt. Other `SymfonyStyle` output methods (`text`, `note`, `block`, ...) happily render inline tags like `<comment>` and `<info>`, so I assumed `ask()` would too:

```php
$io = new SymfonyStyle($input, $output);
$io->ask('Do you want to use Foo\\Bar <comment>or</comment> Foo\\Baz\\?', 'Foo\\Bar');
```

What I expected: the word `or` shows up styled (yellow / comment color), so the prompt visually distinguishes the two choices.

What I actually get: the tags are printed verbatim. The terminal shows the literal string `<comment>or</comment>` as part of the question, as if the whole thing went through some escaping pass before being formatted. The default value (`[Foo\Bar]`) on the other hand renders correctly, so the trailing-backslash handling is fine — it's specifically the inline tags inside the question that come out wrong.

It feels inconsistent that `$io->text('use Foo\\Bar <comment>or</comment> Foo\\Baz')` renders the tag, but `$io->ask('use Foo\\Bar <comment>or</comment> Foo\\Baz?')` does not. Same component, same kind of message, very different behavior.

If it matters: I noticed the same thing on `SymfonyStyle::title()` / `SymfonyStyle::section()` when I tried to put a `<comment>`-highlighted word inside the title — the tag shows up as literal text there too, instead of being rendered.

Tested on the `2.7` branch.
