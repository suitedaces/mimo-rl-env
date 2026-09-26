我想在 v2 的 `.ahoy.yml` 里给命令写更详细的 `description`，不然现在 `ahoy --help` / `ahoy <cmd> --help` 只看得到 usage，长说明写了也像没生效一样。顺手也想把 v2 这些开发命令整理一下：build 相关走 goreleaser，加个 release 命令，旧的 godep 别名就不用留了。

Expected outcomes:
- Command descriptions: a command-level `description:` in a v2 `.ahoy.yml` command is treated as user-visible help text, including descriptions written as YAML multiline block strings.
- Per-command help: `ahoy <cmd> --help` shows the command’s `description:` content when it is configured, while commands without a description continue to work normally.
- Global help: `ahoy --help` shows configured descriptions in the `COMMANDS:` section in addition to each command’s `usage:` summary; multiline descriptions remain readable as multiple lines, and commands without descriptions still show only their normal summary.
- v2 development commands: in the repository’s v2 `.ahoy.yml`, `build` uses `goreleaser build --config ../.goreleaser.yml --snapshot --clean --single-target`, and `build-all` uses `goreleaser build --config ../.goreleaser.yml --snapshot --clean`.
- v2 release command: the repository’s v2 `.ahoy.yml` defines a `release` command that runs `goreleaser release --config ../.goreleaser.yml --clean`.
- v2 dependency command cleanup: the repository’s v2 `.ahoy.yml` no longer defines the old `godep` alias command.

Implementation notes:
- Preserve existing v2 command behavior except where the configured help text or the listed development commands are intentionally changed.
- The data flow, formatting mechanism, and validation location for command descriptions are implementation choices, as long as the observable help output and command configuration behavior match the outcomes above.
- Keep the help output readable for both single-line and multiline descriptions without requiring callers to use a different command-line entry point.
