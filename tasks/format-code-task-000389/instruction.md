Rule can't contain an address and netmask if the connection-type is 'local' with 3.9.0
<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release and devel branch are affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY
<!--- Explain the problem briefly below -->

We got the following snippet in our playbooks:

```
- name: "Enable datata access to its PostgreSQL DB"
  become: true
  become_user: postgres
  community.postgresql.postgresql_pg_hba:
    dest: "/var/lib/pgsql/data/pg_hba.conf"
    contype: local
    databases: datadata
    users: datata
  notify: Restart PostgreSQL
```

That is working flawless since quite some time. With the release of 3.9.0 things started failing with the following:

```
{
  "msg": "Error modifying rules:\nRule can't contain an address and netmask if the connection-type is 'local'",
  "invocation": {
    "module_args": {
      "dest": "/var/lib/pgsql/data/pg_hba.conf",
      "contype": "local",
      "databases": "datadata",
      "users": "datadata",
      "method": "md5",
      "address": "samehost",
      "backup": false,
      "create": false,
      "keep_comments_at_rules": false,
      "state": "present",
      "rules_behavior": "conflict",
      "overwrite": false,
      "unsafe_writes": false,
      "backup_file": null,
      "comment": null,
      "netmask": null,
      "options": null,
      "rules": null,
      "mode": null,
      "owner": null,
      "group": null,
      "seuser": null,
      "serole": null,
      "selevel": null,
      "setype": null,
      "attributes": null
    }
  },
  "_ansible_no_log": false,
  "changed": false
}
```
:top: this is a json from an AWX job.
Pinning the release before that, 3.8.0, gives the expected result.

Trying to pinpoint the issue I've stumbled across https://github.com/ansible-collections/community.postgresql/pull/772 that did some larger refactoring to the handling of parameters, including the `address` that should be omitted if `contype` is set to `local`.
With 3.9.0 the `address` parameter is set to `samehost` if nothing is passed no matter if contype is set to local.
Setting the address to `null`, `~` or leaving it empty results in a `argument 'address' is of type <class 'NoneType'> and we were unable to convert to str: 'None' is not a string and conversion is not allowed`.


##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
<!--- Write the short name of the module, plugin, task or feature below, use your best guess if unsure -->
postgresql.postgresql_pg_hba in Version 3.9.0

##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->

AWX 21.12.0
quay.io/ansible/awx-ee:latest, sha256:7dc75b8723ee9f63ce716fa46f3427895dce756834deeef1d9986af084978c4b

```paste below

```

##### COLLECTION VERSION
<!--- Paste verbatim output from "ansible-galaxy collection list <namespace>.<collection>"  between the quotes
for example: ansible-galaxy collection list community.general
-->
AWX output for collection install:
```paste below
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Downloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/community-rabbitmq-1.3.0.tar.gz to /var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/tmp/ansible-local-5128215awgqocb/tmponshxnzu/community-rabbitmq-1.3.0-b6rwufqd
Installing 'community.rabbitmq:1.3.0' to '/var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/requirements_collections/ansible_collections/community/rabbitmq'
community.rabbitmq:1.3.0 was installed successfully
Downloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/lvrfrc87-git_acp-2.2.0.tar.gz to /var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/tmp/ansible-local-5128215awgqocb/tmponshxnzu/lvrfrc87-git_acp-2.2.0-pji0andp
Installing 'lvrfrc87.git_acp:2.2.0' to '/var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/requirements_collections/ansible_collections/lvrfrc87/git_acp'
lvrfrc87.git_acp:2.2.0 was installed successfully
Downloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/ansible-posix-1.6.2.tar.gz to /var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/tmp/ansible-local-5128215awgqocb/tmponshxnzu/ansible-posix-1.6.2-e7mpoidi
Installing 'ansible.posix:1.6.2' to '/var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/requirements_collections/ansible_collections/ansible/posix'
ansible.posix:1.6.2 was installed successfully
Downloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/ansible-utils-5.1.2.tar.gz to /var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/tmp/ansible-local-5128215awgqocb/tmponshxnzu/ansible-utils-5.1.2-sxszhlbz
Installing 'ansible.utils:5.1.2' to '/var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/requirements_collections/ansible_collections/ansible/utils'
ansible.utils:5.1.2 was installed successfully
Downloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/community-postgresql-3.9.0.tar.gz to /var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/tmp/ansible-local-5128215awgqocb/tmponshxnzu/community-postgresql-3.9.0-ixg1kvij
Installing 'community.postgresql:3.9.0' to '/var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/requirements_collections/ansible_collections/community/postgresql'
community.postgresql:3.9.0 was installed successfully
Downloading https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/artifacts/community-general-10.1.0.tar.gz to /var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/tmp/ansible-local-5128215awgqocb/tmponshxnzu/community-general-10.1.0-gnw0es34
Installing 'community.general:10.1.0' to '/var/lib/awx/projects/.__awx_cache/_23__extrusionos_via_ansible/stage/requirements_collections/ansible_collections/community/general'
community.general:10.1.0 was installed successfully
```

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
No idea how to gather this in AWX.
```paste below

```

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->
AWX 21.12.0


##### STEPS TO REPRODUCE
<!--- Describe exactly how to reproduce the problem, using a minimal test-case -->

<!--- Paste example playbooks or commands between quotes below -->
```yaml
- name: "Enable datata access to its PostgreSQL DB"
  become: true
  become_user: postgres
  community.postgresql.postgresql_pg_hba:
    dest: "/var/lib/pgsql/data/pg_hba.conf"
    contype: local
    databases: datadata
    users: datata
  notify: Restart PostgreSQL
```

<!--- HINT: You can paste gist.github.com links for larger files -->

##### EXPECTED RESULTS
<!--- Describe what you expected to happen when running the steps above -->
Should work without failure like it did in 3.8.0.

##### ACTUAL RESULTS
<!--- Describe what actually happened. If possible run with extra verbosity (-vvvv) -->

<!--- Paste verbatim command output between quotes -->
```paste below
{
  "msg": "Error modifying rules:\nRule can't contain an address and netmask if the connection-type is 'local'",
  "invocation": {
    "module_args": {
      "dest": "/var/lib/pgsql/data/pg_hba.conf",
      "contype": "local",
      "databases": "datadata",
      "users": "datadata",
      "method": "md5",
      "address": "samehost",
      "backup": false,
      "create": false,
      "keep_comments_at_rules": false,
      "state": "present",
      "rules_behavior": "conflict",
      "overwrite": false,
      "unsafe_writes": false,
      "backup_file": null,
      "comment": null,
      "netmask": null,
      "options": null,
      "rules": null,
      "mode": null,
      "owner": null,
      "group": null,
      "seuser": null,
      "serole": null,
      "selevel": null,
      "setype": null,
      "attributes": null
    }
  },
  "_ansible_no_log": false,
  "changed": false
}
```
