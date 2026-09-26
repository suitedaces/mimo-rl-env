我现在用 `darker` 的时候想临时按项目外的 Black 设置来跑，比如这次要换个 line length，或者保留字符串引号别被规范化，但好像只能靠 Black 配置文件控制。能不能让 `darker` 命令行里也能直接传这些 Black 格式化选项，而且我手动传的时候就按我这次传的来？

Expected outcomes:
- CLI line length: `darker` accepts `-l LINE_LENGTH` and `--line-length LINE_LENGTH`, and formatting uses the provided maximum line length for the current run.
- CLI string normalization: `darker` accepts `-S` and `--skip-string-normalization`, and formatting preserves string quotes and prefixes instead of normalizing them for the current run.
- CLI precedence over config: when `-c/--config` is used together with an explicit CLI line-length or skip-string-normalization option, the explicit CLI value takes precedence over the corresponding Black config setting for that run.
- Config compatibility: when a Black configuration read through `-c/--config` requests skipped string normalization, `darker` formats consistently with that configuration.
- User-facing help and documentation: `darker --help` and the README document the supported Black-related command-line options, including `-l/--line-length` and `-S/--skip-string-normalization`.

Implementation notes:
- Keep the behavior compatible with existing `darker` workflows, including formatting only the relevant changed portions.
- The internal representation of option values, where configuration is merged, and how formatting options are passed through are implementation details.
- Preserve existing command-line behavior for users who do not pass the new options.
