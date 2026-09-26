## Issue

In tox <4 using --workdir would override whatever was in tox.ini, this no longer works in >= 4 which makes some CI/CD use cases difficult 

## Environment

Provide at least:

- OS: linux

## Minimal example

If possible, provide a minimal reproducer for the issue:

```
tox.ini:
[tox]
toxworkdir=/tmp/blah

[testenv]
allowlist_externals=echo
commands=echo {toxworkdir}

setup.py
from distutils.core import setup

setup(name='Distutilsaaa',
      version='1.0',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['distutilsa'],
     )

distutilsa/__init.py

```

Tox 4:
```
 jabbera    toxbug   3.8.10  ﮫ20.419s⠀   tox -e py --workdir /tmp/blah1  70  19:30:47 
.pkg: install_requires> python -I -m pip install 'setuptools>=40.8.0' wheel
.pkg: _optional_hooks> python /home/jabbera/.local/lib/python3.10/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: get_requires_for_build_sdist> python /home/jabbera/.local/lib/python3.10/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: prepare_metadata_for_build_wheel> python /home/jabbera/.local/lib/python3.10/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
.pkg: build_sdist> python /home/jabbera/.local/lib/python3.10/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
py: install_package> python -I -m pip install --force-reinstall --no-deps /tmp/blah/.tmp/package/1/Distutilsaaa-1.0.tar.gz
py: commands[0]> echo /tmp/blah
/tmp/blah
.pkg: _exit> python /home/jabbera/.local/lib/python3.10/site-packages/pyproject_api/_backend.py True setuptools.build_meta __legacy__
  py: OK (6.34=setup[6.34]+cmd[0.00] seconds)
  congratulations :) (6.43 seconds)
```

Tox 3:
```
 jabbera    toxbug   3.8.10  ﮫ4.404s⠀   tox -e py --workdir /tmp/blah1         bash   70  19:29:36 
GLOB sdist-make: /home/jabbera/toxbug/setup.py
py inst-nodeps: /tmp/blah1/.tmp/package/1/Distutilsaaa-1.0.zip
py installed: Distutilsaaa @ file:///tmp/blah1/.tmp/package/1/Distutilsaaa-1.0.zip
py run-test-pre: PYTHONHASHSEED='1612454640'
py run-test: commands[0] | echo /tmp/blah1
/tmp/blah1
_______________________________________________________ summary ________________________________________________________
  py: commands succeeded
  congratulations :)
```
