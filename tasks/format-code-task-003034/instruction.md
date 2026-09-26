### C# diagnostics only highlight a single point instead of the actual range

When I work on a C# project with ycmd + OmniSharp, diagnostics (especially warnings) only mark a single character position rather than the span of code they actually refer to. For instance, a warning about an unused variable or a redundant cast highlights just the starting column of the identifier, while in other completers (and in OmniSharp's own clients) the whole token / expression gets underlined.

Looking at what comes back from the OmniSharp server, the `QuickFix` entries do contain a valid end position for most diagnostics — it's just that ycmd seems to collapse the diagnostic range down to its start, so the end information is thrown away before it reaches the editor.

It would be great if the C# completer preserved the range OmniSharp gives us, so editors can highlight the full extent of a diagnostic the same way they do for other languages. For diagnostics where the server doesn't supply a meaningful end position, the current single-point behaviour is fine as a fallback.
