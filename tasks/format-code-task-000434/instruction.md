dredd init generates invalid file
**Describe the bug**
I ran `dredd init` which generates a `dredd.yml` config file.
When I run `dredd --dry-run` I get the following error:

```
error: unknown tag !<tag:yaml.org,2002:js/undefined> at line 4, column 47:
     ... g:yaml.org,2002:js/undefined> ''
```

Looking in the generated config there is this line:
```yaml
language: !<tag:yaml.org,2002:js/undefined> ''
```

This seems to be what is broken.

Deleting that line fixes the problem.

**What's your `dredd --version` output?**

```
dredd v8.0.0 (Darwin 18.2.0; x64)
```
