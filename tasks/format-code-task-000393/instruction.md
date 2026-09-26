Double-nested ansible_collections folders cause errors
# Issue Type

- Bug report

# Molecule and Ansible details

ansible - 3.1.0
ansible-base - 2.10.6
molecule - 3.2.3

Molecule installation method (one of):

- pip

Ansible installation method (one of):

- pip

# Desired Behavior

Because of some weirdness I'm running my tests under a double folder structure that goes something like

/home/user/src/ansible_collections/some/more/paths/ansible_collections/namespace/collection/roles

When living there, I should still have no issues with running Molecule

# Actual Behaviour

Errors arise from line 424 in molecule/provisioner/ansible.py which assumes that collection_indicator occurs exactly one time in the path structure.

Resulting output:

```console
$ tox -e roles-test_role-docker
roles-test_role-docker installed: ansible==3.1.0,ansible-base==2.10.5,ansible-lint==5.0.3,appdirs==1.4.4,arrow==1.0.3,attrs==20.3.0,bcrypt==3.2.0,binaryornot==0.4.4,boto==2.49.0,boto3==1.17.25,botocore==1.20.25,bracex==2.1.1,Cerberus==1.3.2,certifi==2020.12.5,cffi==1.14.5,chardet==4.0.0,click==7.1.2,click-completion==0.5.2,click-help-colors==0.9,colorama==0.4.4,commonmark==0.9.1,cookiecutter==1.7.2,cryptography==3.4.6,decorator==4.4.2,distro==1.5.0,docker==4.4.4,dogpile.cache==1.1.2,enrich==1.2.6,flake8==3.8.4,idna==2.10,iniconfig==1.1.1,iso8601==0.1.14,Jinja2==2.11.3,jinja2-time==0.2.0,jmespath==0.10.0,jsonpatch==1.31,jsonpointer==2.0,keystoneauth1==4.3.1,MarkupSafe==1.1.1,mccabe==0.6.1,molecule==3.2.2,molecule-containers==0.2.1,molecule-docker==0.2.4,molecule-ec2==0.3,molecule-openstack==0.3,molecule-podman==0.3.0,molecule-vagrant==0.6.1,munch==2.5.0,netifaces==0.10.9,openstacksdk==0.54.0,os-client-config==2.1.0,os-service-types==1.7.0,packaging==20.9,paramiko==2.7.2,pathspec==0.8.1,pbr==5.5.1,pluggy==0.13.1,poyo==0.5.0,py==1.10.0,pycodestyle==2.6.0,pycparser==2.20,pyflakes==2.2.0,Pygments==2.8.1,PyNaCl==1.4.0,pyparsing==2.4.7,pytest==6.2.2,pytest-testinfra==6.1.0,python-dateutil==2.8.1,python-slugify==4.0.1,PyYAML==5.4.1,requests==2.25.1,requestsexceptions==1.4.0,rich==9.13.0,ruamel.yaml==0.16.13,ruamel.yaml.clib==0.2.2,s3transfer==0.3.4,selinux==0.2.1,shellingham==1.4.0,six==1.15.0,stevedore==3.3.0,subprocess-tee==0.2.0,testinfra==6.0.0,text-unidecode==1.3,toml==0.10.2,typing-extensions==3.7.4.3,urllib3==1.26.3,wcmatch==8.1.2,websocket-client==0.58.0,yamllint==1.26.0
roles-test_role-docker run-test-pre: PYTHONHASHSEED='4259097906'
roles-test_role-docker run-test: commands[0] | molecule --debug -c /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/tests/molecule.yml test -s docker
DEBUG    Validating schema /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker/molecule.yml.
INFO     docker scenario test matrix: dependency, lint, cleanup, destroy, syntax, create, prepare, converge, idempotence, side_effect, verify, cleanup, destroy
INFO     Running docker > dependency
DEBUG: ANSIBLE ENVIRONMENT:
ANSIBLE_COLLECTIONS_PATH: /var/home/ghelling/src/:/var/home/ghelling/.ansible
ANSIBLE_COLLECTIONS_PATHS: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/../../../
ANSIBLE_FORCE_COLOR: '1'

DEBUG: MOLECULE ENVIRONMENT:
MOLECULE_DEBUG: 'True'
MOLECULE_DEPENDENCY_NAME: galaxy
MOLECULE_DRIVER_NAME: docker
MOLECULE_ENV_FILE: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/.env.yml
MOLECULE_EPHEMERAL_DIRECTORY: /var/home/ghelling/.cache/molecule/test_role/docker
MOLECULE_FILE: /var/home/ghelling/.cache/molecule/test_role/docker/molecule.yml
MOLECULE_INSTANCE_CONFIG: /var/home/ghelling/.cache/molecule/test_role/docker/instance_config.yml
MOLECULE_INVENTORY_FILE: /var/home/ghelling/.cache/molecule/test_role/docker/inventory/ansible_inventory.yml
MOLECULE_PROJECT_DIRECTORY: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role
MOLECULE_PROVISIONER_NAME: ansible
MOLECULE_SCENARIO_DIRECTORY: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker
MOLECULE_SCENARIO_NAME: docker
MOLECULE_STATE_FILE: /var/home/ghelling/.cache/molecule/test_role/docker/state.yml
MOLECULE_VERIFIER_NAME: testinfra
MOLECULE_VERIFIER_TEST_DIRECTORY: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker/tests

DEBUG: SHELL REPLAY:
ANSIBLE_COLLECTIONS_PATH=/var/home/ghelling/src/:/var/home/ghelling/.ansible ANSIBLE_COLLECTIONS_PATHS=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/../../../ ANSIBLE_FORCE_COLOR=1 MOLECULE_DEBUG=True MOLECULE_DEPENDENCY_NAME=galaxy MOLECULE_DRIVER_NAME=docker MOLECULE_ENV_FILE=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/.env.yml MOLECULE_EPHEMERAL_DIRECTORY=/var/home/ghelling/.cache/molecule/test_role/docker MOLECULE_FILE=/var/home/ghelling/.cache/molecule/test_role/docker/molecule.yml MOLECULE_INSTANCE_CONFIG=/var/home/ghelling/.cache/molecule/test_role/docker/instance_config.yml MOLECULE_INVENTORY_FILE=/var/home/ghelling/.cache/molecule/test_role/docker/inventory/ansible_inventory.yml MOLECULE_PROJECT_DIRECTORY=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role MOLECULE_PROVISIONER_NAME=ansible MOLECULE_SCENARIO_DIRECTORY=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker MOLECULE_SCENARIO_NAME=docker MOLECULE_STATE_FILE=/var/home/ghelling/.cache/molecule/test_role/docker/state.yml MOLECULE_VERIFIER_NAME=testinfra MOLECULE_VERIFIER_TEST_DIRECTORY=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker/tests

COMMAND: ansible-galaxy install --force --role-file ../../requirements.yml --roles-path /var/home/ghelling/.cache/molecule/test_role/docker/roles -vvv
ansible-galaxy 2.10.5
  config file = /var/home/ghelling/.ansible.cfg
  configured module search path = ['/var/home/ghelling/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/ansible
  executable location = /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/bin/ansible-galaxy
  python version = 3.9.1 (default, Dec  8 2020, 00:00:00) [GCC 10.2.1 20201125 (Red Hat 10.2.1-9)]
Using /var/home/ghelling/.ansible.cfg as config file
Reading requirement file at '/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/requirements.yml'
[WARNING]: The requirements file '/var/home/ghelling/src/ansible_collections/me
ta_ansible_templates/ansible_collections/test_ns/test_collection/requirements.y
ml' contains collections which will be ignored. To install these collections
run 'ansible-galaxy collection install -r' or to install both at the same time
run 'ansible-galaxy install -r' without a custom install path.
Skipping install, no requirements found
INFO     Dependency completed successfully.
DEBUG: ANSIBLE ENVIRONMENT:
ANSIBLE_COLLECTIONS_PATH: /var/home/ghelling/.cache/molecule/test_role/docker/collections
ANSIBLE_COLLECTIONS_PATHS: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/../../../
ANSIBLE_FORCE_COLOR: '1'

DEBUG: MOLECULE ENVIRONMENT:
MOLECULE_DEBUG: 'True'
MOLECULE_DEPENDENCY_NAME: galaxy
MOLECULE_DRIVER_NAME: docker
MOLECULE_ENV_FILE: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/.env.yml
MOLECULE_EPHEMERAL_DIRECTORY: /var/home/ghelling/.cache/molecule/test_role/docker
MOLECULE_FILE: /var/home/ghelling/.cache/molecule/test_role/docker/molecule.yml
MOLECULE_INSTANCE_CONFIG: /var/home/ghelling/.cache/molecule/test_role/docker/instance_config.yml
MOLECULE_INVENTORY_FILE: /var/home/ghelling/.cache/molecule/test_role/docker/inventory/ansible_inventory.yml
MOLECULE_PROJECT_DIRECTORY: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role
MOLECULE_PROVISIONER_NAME: ansible
MOLECULE_SCENARIO_DIRECTORY: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker
MOLECULE_SCENARIO_NAME: docker
MOLECULE_STATE_FILE: /var/home/ghelling/.cache/molecule/test_role/docker/state.yml
MOLECULE_VERIFIER_NAME: testinfra
MOLECULE_VERIFIER_TEST_DIRECTORY: /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker/tests

DEBUG: SHELL REPLAY:
ANSIBLE_COLLECTIONS_PATH=/var/home/ghelling/.cache/molecule/test_role/docker/collections ANSIBLE_COLLECTIONS_PATHS=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/../../../ ANSIBLE_FORCE_COLOR=1 MOLECULE_DEBUG=True MOLECULE_DEPENDENCY_NAME=galaxy MOLECULE_DRIVER_NAME=docker MOLECULE_ENV_FILE=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/.env.yml MOLECULE_EPHEMERAL_DIRECTORY=/var/home/ghelling/.cache/molecule/test_role/docker MOLECULE_FILE=/var/home/ghelling/.cache/molecule/test_role/docker/molecule.yml MOLECULE_INSTANCE_CONFIG=/var/home/ghelling/.cache/molecule/test_role/docker/instance_config.yml MOLECULE_INVENTORY_FILE=/var/home/ghelling/.cache/molecule/test_role/docker/inventory/ansible_inventory.yml MOLECULE_PROJECT_DIRECTORY=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role MOLECULE_PROVISIONER_NAME=ansible MOLECULE_SCENARIO_DIRECTORY=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker MOLECULE_SCENARIO_NAME=docker MOLECULE_STATE_FILE=/var/home/ghelling/.cache/molecule/test_role/docker/state.yml MOLECULE_VERIFIER_NAME=testinfra MOLECULE_VERIFIER_TEST_DIRECTORY=/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/roles/test_role/molecule/docker/tests

COMMAND: ansible-galaxy collection install --collections-path /var/home/ghelling/.cache/molecule/test_role/docker/collections --force --requirements-file ../../requirements.yml -vvv
ansible-galaxy 2.10.5
  config file = /var/home/ghelling/.ansible.cfg
  configured module search path = ['/var/home/ghelling/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/ansible
  executable location = /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/bin/ansible-galaxy
  python version = 3.9.1 (default, Dec  8 2020, 00:00:00) [GCC 10.2.1 20201125 (Red Hat 10.2.1-9)]
Using /var/home/ghelling/.ansible.cfg as config file
Reading requirement file at '/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/requirements.yml'
Starting galaxy collection install process
Found installed collection oasis_roles.system:1.1.2 at '/var/home/ghelling/.cache/molecule/test_role/docker/collections/ansible_collections/oasis_roles/system'
Process install dependency map
Processing requirement collection 'oasis_roles.system'
Opened /var/home/ghelling/.ansible/galaxy_token
Collection 'oasis_roles.system' obtained from server default https://galaxy.ansible.com/api/
Starting collection install process
Installing 'oasis_roles.system:1.1.2' to '/var/home/ghelling/.cache/molecule/test_role/docker/collections/ansible_collections/oasis_roles/system'
Downloading https://galaxy.ansible.com/download/oasis_roles-system-1.1.2.tar.gz to /var/home/ghelling/.ansible/tmp/ansible-local-19703xsl957j9/tmponq_48k7
oasis_roles.system (1.1.2) was installed successfully
INFO     Dependency completed successfully.
INFO     Running docker > lint
INFO     Lint is disabled.
INFO     Running docker > cleanup
WARNING  Skipping, cleanup playbook not configured.
INFO     Running docker > destroy
Traceback (most recent call last):
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/bin/molecule", line 10, in <module>
    sys.exit(main())
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/click/core.py", line 829, in __call__
    return self.main(*args, **kwargs)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/click/core.py", line 782, in main
    rv = self.invoke(ctx)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/click/core.py", line 1259, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/click/core.py", line 1066, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/click/core.py", line 610, in invoke
    return callback(*args, **kwargs)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/click/decorators.py", line 21, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/command/test.py", line 149, in test
    base.execute_cmdline_scenarios(scenario_name, args, command_args)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/command/base.py", line 113, in execute_cmdline_scenarios
    execute_scenario(scenario)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/command/base.py", line 155, in execute_scenario
    execute_subcommand(scenario.config, action)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/command/base.py", line 144, in execute_subcommand
    return command(config).execute()
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/logger.py", line 185, in wrapper
    rt = func(*args, **kwargs)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/command/destroy.py", line 107, in execute
    self._config.provisioner.destroy()
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/provisioner/ansible.py", line 702, in destroy
    pb = self._get_ansible_playbook(self.playbooks.destroy)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/provisioner/ansible.py", line 868, in _get_ansible_playbook
    return ansible_playbook.AnsiblePlaybook(playbook, self._config, **kwargs)
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/provisioner/ansible_playbook.py", line 45, in __init__
    self._env = self._config.provisioner.env
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/provisioner/ansible.py", line 519, in env
    default_env = self.default_env
  File "/var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/lib/python3.9/site-packages/molecule/provisioner/ansible.py", line 424, in default_env
    collection_path, right = self._config.project_directory.split(
ValueError: too many values to unpack (expected 2)
ERROR: InvocationError for command /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/.tox/ansible/bin/molecule --debug -c /var/home/ghelling/src/ansible_collections/meta_ansible_templates/ansible_collections/test_ns/test_collection/tests/molecule.yml test -s docker (exited with code 1)
```
