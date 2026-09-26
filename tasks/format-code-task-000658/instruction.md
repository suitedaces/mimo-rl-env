## Problem Statement

I'm still using `docker: true` in some fogg configs, and right now `fogg plan` / `fogg apply` don't give me any heads-up that Docker support is going away. Can we have those commands show a non-fatal deprecation warning when Docker is enabled, and have config validation surface that kind of warning instead of only fatal errors?

## Expected outcomes

- **Docker-enabled CLI runs**
  - When a configuration enables Docker with `docker: true`, both `fogg plan` and `fogg apply` should emit the warning `Docker support is deprecated and will be removed in a future version of fogg.`
  - That warning is non-fatal: it should not by itself cause `fogg plan` or `fogg apply` to fail.

- **Docker-disabled CLI runs**
  - When Docker is not enabled in the configuration, `fogg plan` and `fogg apply` should not emit the Docker deprecation warning.

- **Configuration validation warnings**
  - `config/v2.Config.Validate` should surface non-fatal validation warnings as well as fatal validation errors.
  - Calling `Validate` on a config whose `Docker` setting is true should return a warning containing `Docker support is deprecated and will be removed in a future version of fogg.`
  - Fatal validation failures should still be reported as errors; non-fatal warnings should remain inspectable even when fatal validation errors are also present.

## Implementation notes

The exact mechanism for collecting, propagating, and displaying warnings is up to the implementation. Keep existing fatal validation behavior intact while adding a way for callers and CLI commands to observe non-fatal warnings.
