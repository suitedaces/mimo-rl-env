The built-in Fx event loggers currently treat several failed option events as if they partly succeeded: a failed `Provided`, `Replaced`, or `Decorated` event can emit one success record per output followed by an error, while Zap records some failures at Info and omits useful event context. Make failure logging atomic and consistent across `fxevent.ZapLogger` and `fxevent.ConsoleLogger`.

For `OnStartExecuted` and `OnStopExecuted` events with a non-nil `Err`, Zap must emit exactly one Error-level entry using the existing messages (`OnStart hook failed` and `OnStop hook failed`). Its fields must be exactly `callee`, `caller`, `runtime`, and `error`, with runtime rendered using `time.Duration.String()`. Console must continue to emit one failure line containing the hook kind, callee, caller, runtime, and error. Successful hook-event behavior remains unchanged.

Treat `Supplied`, `Provided`, `Replaced`, and `Decorated` as outcome events. When `Err` is non-nil, each built-in logger must emit exactly one failure record and no success records, even if `OutputTypeNames` has multiple entries or is empty. Zap uses Error level and these exact messages and fields:

- `Supplied`: message `supply failed`; fields `type`, optional `module`, and `error`.
- `Provided`: message `provide failed`; fields `constructor`, optional `module`, ordered string-array field `types`, and `error`.
- `Replaced`: message `replace failed`; fields optional `module`, ordered string-array field `types`, and `error`.
- `Decorated`: message `decorate failed`; fields `decorator`, optional `module`, ordered string-array field `types`, and `error`.

For ConsoleLogger, failure lines must use the `[Fx] ERROR\t` prefix and these forms:

- `Failed to supply <type><module>: <error>`
- `Failed to provide [<types>] from <constructor><module>: <error>`
- `Failed to replace [<types>]<module>: <error>`
- `Failed to decorate [<types>] with <decorator><module>: <error>`

Here `<module>` is ` from module %q` when `ModuleName` is non-empty and is omitted otherwise. Format `<types>` in event order, separated by comma and space; an empty list renders as `[]`. Errors use their normal `Error()` text.

When these four events have a nil `Err`, preserve the established behavior: `Supplied` logs one Info/supply record, while `Provided`, `Replaced`, and `Decorated` log one Info/success record per output type in event order with their existing messages and fields. Keep the behavior of all other event variants unchanged.
