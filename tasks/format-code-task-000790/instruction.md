## Dart analysis_server linter still uses the deprecated snapshot command

I recently upgraded my Dart SDK to 2.16, and ALE's `analysis_server` linter for Dart stopped working for me. Opening any `.dart` file no longer gives me diagnostics, completions, or any other LSP features.

Looking at what ALE is invoking, it runs something like:

```
<dart-bin-dir>/snapshots/analysis_server.dart.snapshot --lsp
```

Starting with Dart 2.16, the Dart team added a top-level subcommand for the language server:

```
dart language-server --protocol=lsp
```

and the old `analysis_server.dart.snapshot --lsp` invocation is the deprecated way of starting it (and on some installs the snapshot file isn't even in the expected place anymore). So ALE is effectively hardcoded to the old path.

Could the Dart `analysis_server` linter be updated to use the new `dart language-server` subcommand? It would be nice if people still on older Dart versions (< 2.16) where the new subcommand doesn't exist yet can keep using the old invocation, so this probably needs to be configurable rather than just swapped out. The toggle would probably be something like `g:ale_dart_analysis_server_enable_language_server`.
