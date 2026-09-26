stubgen: Use `Generator[...]` instead of `Generator[..., None, None]`
Typeshed now uses default of `None` for the second and third argument to `Generator` and we've started to change instances of `Generator[..., None, None]` to just `Generator[...]`. For readability and consistency, stubgen should do the same.
