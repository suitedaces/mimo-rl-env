## `credential` module gives a confusing error when `credential_type` is omitted

I'm using the `ansible.controller.credential` module (from the awx collection) to manage credentials against an AWX 23.4.x controller. I had a typo in my playbook and forgot to specify `credential_type`. Instead of telling me the parameter was missing, the module failed with an unrelated-looking error from somewhere deeper in the module.

Roughly what I had:

```yaml
- name: Add machine credential
  ansible.controller.credential:
    name: my-cred
    organization: Default
    # credential_type accidentally omitted
    state: present
    inputs:
      username: joe
      password: secret
```

When I run this, the task fails, but the error message doesn't make it obvious that the problem is just a missing parameter — it looks like something went wrong internally. It took me a while to realize I'd simply forgotten `credential_type`.

Looking at the module docs, `credential_type` doesn't seem to be marked as required, even though in practice you basically always need it to create/look up a credential. It would be much friendlier if the module treated it as a required parameter and failed up front with a clear "missing required argument" message, the same way `name` already does.
