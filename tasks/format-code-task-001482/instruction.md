## `!include_dir_named` silently drops empty YAML files

I split my automations / scripts into one file per item using `!include_dir_named`, e.g.

```yaml
script: !include_dir_named scripts/
```

with a `scripts/` folder like:

```
scripts/
  morning.yaml
  evening.yaml
  placeholder.yaml   # empty for now, I'll fill it in later
```

I'd expect the resulting mapping to have three keys: `morning`, `evening`, `placeholder` — with `placeholder` being effectively empty. Instead, the `placeholder` key is missing from the dict altogether, as if the file didn't exist. The same thing happens to any file that only contains a comment or is otherwise "empty" from YAML's point of view.

This is surprising because the filename is supposed to become a key in the mapping regardless of contents, and it makes it impossible to keep around stub files. It also means iterating over the loaded mapping silently skips entries that exist on disk, which is annoying to debug — you have to notice the key is missing and then go check whether the file happens to be empty.

Could `!include_dir_named` keep the key for empty files instead of dropping them?
