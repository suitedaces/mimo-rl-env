### Feature request: allow the `community.general.sudoers` module to produce rules that preserve environment variables

I'm using `community.general.sudoers` to manage `/etc/sudoers.d` entries on my hosts. One of my users (let's call her `alice`) needs to run a small upload script via sudo:

```yaml
- name: Allow alice to sudo /usr/local/bin/upload
  community.general.sudoers:
    name: allow-alice-upload
    user: alice
    commands: /usr/local/bin/upload
```

The script she's running depends on a couple of environment variables that are configured in her shell (things like `AWS_PROFILE`, `HTTP_PROXY`, and a custom `PATH` addition). When she runs the command through sudo, those variables get stripped, so the script fails because the config it expects isn't there.

If I were hand-writing the sudoers file I would just slap the `SETENV` tag on the rule, e.g.:

```
alice ALL=(ALL) SETENV: /usr/local/bin/upload
```

That way she can invoke it with `sudo -E /usr/local/bin/upload` (or `sudo FOO=bar /usr/local/bin/upload`) and the environment is preserved. This is a pretty standard sudoers feature.

As far as I can tell, the `sudoers` module doesn't currently expose any way to emit this tag in the generated rule. There's already an option that controls whether `NOPASSWD:` is included, but nothing equivalent for `SETENV:`, so the only workaround is to stop using the module for these rules and drop a hand-written file into `/etc/sudoers.d`, which defeats the purpose.

Could the module be extended to optionally include `SETENV:` in the rule it writes? Existing playbooks should keep behaving the same by default — I'd only want this turned on for the rules where I explicitly ask for it.
