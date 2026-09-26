Deleting lock file, in combination with `--remove-untracked`, causes packages to be removed during install
- [x] I am on the [latest](https://github.com/python-poetry/poetry/releases/latest) Poetry version.
- [x] I have searched the [issues](https://github.com/python-poetry/poetry/issues) of this repo and believe that this is not a duplicate.
- [x] If an exception occurs when executing a command, I executed it again in debug mode (`-vvv` option).

- **OS version and name**: Ubuntu 18.04
- **Poetry version**:  1.1.8

## Issue
In my workflow I need to remove lock file before running `poetry install` (so essentially Poetry does dependency resolution form scratch). I also use `--remove-untracked` flag.

My dependencies are as follows (though I don't think it matters what the actual dependencies are):

```toml
[tool.poetry.dependencies]
python = ">=3.6"
numpy = ">=1.13.0"
pandas = ">=0.14.0"

[tool.poetry.dev-dependencies]
cython = ">=0.20"
pytest = ">=2.5"
```

On the first run, in all installs properly:
```bash
$ rm -f ./poetry.lock
$ poetry install --remove-untracked
Updating dependencies
Resolving dependencies... (0.4s)

Writing lock file

Package operations: 17 installs, 0 updates, 0 removals

  • Installing typing-extensions (3.10.0.2)
  • Installing zipp (3.5.0)
  • Installing importlib-metadata (4.8.1)
  • Installing pyparsing (2.4.7)
  • Installing six (1.16.0)
  • Installing attrs (21.2.0)
  • Installing iniconfig (1.1.1)
  • Installing numpy (1.19.5)
  • Installing packaging (21.0)
  • Installing pluggy (1.0.0)
  • Installing py (1.10.0)
  • Installing python-dateutil (2.8.2)
  • Installing pytz (2021.1)
  • Installing toml (0.10.2)
  • Installing cython (0.29.24)
  • Installing pandas (0.25.3)
  • Installing pytest (6.2.5)

Installing the current project: <...>
```

Upon repeating the same commands, however, it ends up removing the dependencies (while it generates an identical lock file to the one I deleted)!

```bash
$ rm -f ./poetry.lock
$ poetry install --remove-untracked
Updating dependencies
Resolving dependencies... (0.4s)

Writing lock file

Package operations: 0 installs, 0 updates, 17 removals

  • Removing attrs (21.2.0)
  • Removing cython (0.29.24)
  • Removing importlib-metadata (4.8.1)
  • Removing iniconfig (1.1.1)
  • Removing numpy (1.19.5)
  • Removing packaging (21.0)
  • Removing pandas (0.25.3)
  • Removing pluggy (1.0.0)
  • Removing py (1.10.0)
  • Removing pyparsing (2.4.7)
  • Removing pytest (6.2.5)
  • Removing python-dateutil (2.8.2)
  • Removing pytz (2021.1)
  • Removing six (1.16.0)
  • Removing toml (0.10.2)
  • Removing typing-extensions (3.10.0.2)
  • Removing zipp (3.5.0)

Installing the current project: <...>
```
which then obviously fails since all the dependencies are missing. It then goes in a circle - next run installs the packages, and the following removes them again. Re-running with `-vvv` gives a hint as to what may be happening:

```bash
$ rm -f ./poetry.lock
$ poetry install --remove-untracked -vvv
$ Using virtualenv: <...>
Updating dependencies
Resolving dependencies...
   1: fact: <...> is 0.1.0
   1: derived: <...>
   1: fact: <...> depends on numpy (>=1.13.0)
   1: fact: <...> depends on pandas (>=0.14.0)
   1: fact: <...> depends on cython (>=0.20)
   1: fact: <...> depends on pytest (>=2.5)
   1: fact: <...> depends on cython (>=0.20)
   1: fact: <...> depends on pytest (>=2.5)
   1: selecting <...> (0.1.0)
   1: derived: pytest (>=2.5)
   1: derived: cython (>=0.20)
   1: derived: pandas (>=0.14.0)
   1: derived: numpy (>=1.13.0)
   1: fact: numpy (1.21.2) requires Python >=3.7,<3.11
   1: derived: not numpy (==1.21.2)
   1: fact: numpy (1.21.1) requires Python >=3.7
   1: derived: not numpy (==1.21.1)
   1: fact: numpy (1.21.0) requires Python >=3.7
   1: derived: not numpy (==1.21.0)
   1: fact: numpy (1.20.3) requires Python >=3.7
   1: derived: not numpy (==1.20.3)
   1: fact: numpy (1.20.2) requires Python >=3.7
   1: derived: not numpy (==1.20.2)
   1: fact: numpy (1.20.1) requires Python >=3.7
   1: derived: not numpy (==1.20.1)
   1: fact: numpy (1.20.0) requires Python >=3.7
   1: derived: not numpy (==1.20.0)
   1: selecting numpy (1.19.5)
   1: fact: pandas (1.3.2) requires Python >=3.7.1
   1: derived: not pandas (==1.3.2)
   1: fact: pandas (1.3.1) requires Python >=3.7.1
   1: derived: not pandas (==1.3.1)
   1: fact: pandas (1.3.0) requires Python >=3.7.1
   1: derived: not pandas (==1.3.0)
   1: fact: pandas (1.2.5) requires Python >=3.7.1
   1: derived: not pandas (==1.2.5)
   1: fact: pandas (1.2.4) requires Python >=3.7.1
   1: derived: not pandas (==1.2.4)
   1: fact: pandas (1.2.3) requires Python >=3.7.1
   1: derived: not pandas (==1.2.3)
   1: fact: pandas (1.2.2) requires Python >=3.7.1
   1: derived: not pandas (==1.2.2)
   1: fact: pandas (1.2.1) requires Python >=3.7.1
   1: derived: not pandas (==1.2.1)
   1: fact: pandas (1.2.0) requires Python >=3.7.1
   1: derived: not pandas (==1.2.0)
   1: fact: pandas (1.1.5) requires Python >=3.6.1
   1: derived: not pandas (==1.1.5)
   1: fact: pandas (1.1.4) requires Python >=3.6.1
   1: derived: not pandas (==1.1.4)
   1: fact: pandas (1.1.3) requires Python >=3.6.1
   1: derived: not pandas (==1.1.3)
   1: fact: pandas (1.1.2) requires Python >=3.6.1
   1: derived: not pandas (==1.1.2)
   1: fact: pandas (1.1.1) requires Python >=3.6.1
   1: derived: not pandas (==1.1.1)
   1: fact: pandas (1.1.0) requires Python >=3.6.1
   1: derived: not pandas (==1.1.0)
   1: fact: pandas (1.0.5) requires Python >=3.6.1
   1: derived: not pandas (==1.0.5)
   1: fact: pandas (1.0.4) requires Python >=3.6.1
   1: derived: not pandas (==1.0.4)
   1: fact: pandas (1.0.3) requires Python >=3.6.1
   1: derived: not pandas (==1.0.3)
   1: fact: pandas (1.0.2) requires Python >=3.6.1
   1: derived: not pandas (==1.0.2)
   1: fact: pandas (1.0.1) requires Python >=3.6.1
   1: derived: not pandas (==1.0.1)
   1: fact: pandas (1.0.0) requires Python >=3.6.1
   1: derived: not pandas (==1.0.0)
   1: fact: pandas (0.25.3) depends on python-dateutil (>=2.6.1)
   1: fact: pandas (0.25.3) depends on pytz (>=2017.2)
   1: fact: pandas (0.25.3) depends on numpy (>=1.13.3)
   1: selecting pandas (0.25.3)
   1: derived: pytz (>=2017.2)
   1: derived: python-dateutil (>=2.6.1)
   1: fact: python-dateutil (2.8.2) depends on six (>=1.5)
   1: selecting python-dateutil (2.8.2)
   1: derived: six (>=1.5)
   1: selecting pytz (2021.1)
   1: selecting six (1.16.0)
   1: selecting cython (0.29.24)
   1: fact: pytest (6.2.5) depends on attrs (>=19.2.0)
   1: fact: pytest (6.2.5) depends on iniconfig (*)
   1: fact: pytest (6.2.5) depends on packaging (*)
   1: fact: pytest (6.2.5) depends on pluggy (>=0.12,<2.0)
   1: fact: pytest (6.2.5) depends on py (>=1.8.2)
   1: fact: pytest (6.2.5) depends on toml (*)
   1: fact: pytest (6.2.5) depends on importlib-metadata (>=0.12)
   1: fact: pytest (6.2.5) depends on atomicwrites (>=1.0)
   1: fact: pytest (6.2.5) depends on colorama (*)
   1: selecting pytest (6.2.5)
   1: derived: colorama
   1: derived: atomicwrites (>=1.0)
   1: derived: importlib-metadata (>=0.12)
   1: derived: toml
   1: derived: py (>=1.8.2)
   1: derived: pluggy (>=0.12,<2.0)
   1: derived: packaging
   1: derived: iniconfig
   1: derived: attrs (>=19.2.0)
   1: selecting py (1.10.0)
   1: fact: pluggy (1.0.0) depends on importlib-metadata (>=0.12)
   1: selecting pluggy (1.0.0)
   1: selecting iniconfig (1.1.1)
   1: selecting attrs (21.2.0)
   1: selecting toml (0.10.2)
   1: fact: packaging (21.0) depends on pyparsing (>=2.0.2)
   1: selecting packaging (21.0)
   1: derived: pyparsing (>=2.0.2)
   1: selecting pyparsing (2.4.7)
   1: selecting atomicwrites (1.4.0)
   1: selecting colorama (0.4.4)
   1: fact: importlib-metadata (4.8.1) depends on zipp (>=0.5)
   1: fact: importlib-metadata (4.8.1) depends on typing-extensions (>=3.6.4)
   1: selecting importlib-metadata (4.8.1)
   1: derived: typing-extensions (>=3.6.4)
   1: derived: zipp (>=0.5)
   1: selecting zipp (3.5.0)
   1: selecting typing-extensions (3.10.0.2)
   1: Version solving took 0.403 seconds.
   1: Tried 1 solutions.

Writing lock file

Finding the necessary packages for the current system

Package operations: 0 installs, 0 updates, 17 removals, 17 skipped

  • Removing attrs (21.2.0): Pending...
  • Removing attrs (21.2.0): Removing...
  • Removing attrs (21.2.0)
  • Removing cython (0.29.24): Pending...
  • Removing cython (0.29.24): Removing...
  • Removing cython (0.29.24)
  • Removing importlib-metadata (4.8.1): Pending...
  • Removing importlib-metadata (4.8.1): Removing...
  • Removing importlib-metadata (4.8.1)
  • Removing iniconfig (1.1.1): Pending...
  • Removing iniconfig (1.1.1): Removing...
  • Removing iniconfig (1.1.1)
  • Removing numpy (1.19.5): Pending...
  • Removing numpy (1.19.5): Removing...
  • Removing numpy (1.19.5)
  • Removing packaging (21.0): Pending...
  • Removing packaging (21.0): Removing...
  • Removing packaging (21.0)
  • Removing pandas (0.25.3): Pending...
  • Removing pandas (0.25.3): Removing...
  • Removing pandas (0.25.3)
  • Removing pluggy (1.0.0): Pending...
  • Removing pluggy (1.0.0): Removing...
  • Removing pluggy (1.0.0)
  • Removing py (1.10.0): Pending...
  • Removing py (1.10.0): Removing...
  • Removing py (1.10.0)
  • Removing pyparsing (2.4.7): Pending...
  • Removing pyparsing (2.4.7): Removing...
  • Removing pyparsing (2.4.7)
  • Removing pytest (6.2.5): Pending...
  • Removing pytest (6.2.5): Removing...
  • Removing pytest (6.2.5)
  • Removing python-dateutil (2.8.2): Pending...
  • Removing python-dateutil (2.8.2): Removing...
  • Removing python-dateutil (2.8.2)
  • Removing pytz (2021.1): Pending...
  • Removing pytz (2021.1): Removing...
  • Removing pytz (2021.1)
  • Removing six (1.16.0): Pending...
  • Removing six (1.16.0): Removing...
  • Removing six (1.16.0)
  • Removing toml (0.10.2): Pending...
  • Removing toml (0.10.2): Removing...
  • Removing toml (0.10.2)
  • Removing typing-extensions (3.10.0.2): Pending...
  • Removing typing-extensions (3.10.0.2): Removing...
  • Removing typing-extensions (3.10.0.2)
  • Removing zipp (3.5.0): Pending...
  • Removing zipp (3.5.0): Removing...
  • Removing zipp (3.5.0)
  • Installing typing-extensions (3.10.0.2): Pending...
  • Installing typing-extensions (3.10.0.2): Skipped for the following reason: Already installed
  • Installing zipp (3.5.0): Pending...
  • Installing zipp (3.5.0): Skipped for the following reason: Already installed
  • Installing importlib-metadata (4.8.1): Pending...
  • Installing importlib-metadata (4.8.1): Skipped for the following reason: Already installed
  • Installing pyparsing (2.4.7): Pending...
  • Installing pyparsing (2.4.7): Skipped for the following reason: Already installed
  • Installing six (1.16.0): Pending...
  • Installing six (1.16.0): Skipped for the following reason: Already installed
  • Installing attrs (21.2.0): Pending...
  • Installing attrs (21.2.0): Skipped for the following reason: Already installed
  • Installing iniconfig (1.1.1): Pending...
  • Installing iniconfig (1.1.1): Skipped for the following reason: Already installed
  • Installing numpy (1.19.5): Pending...
  • Installing numpy (1.19.5): Skipped for the following reason: Already installed
  • Installing packaging (21.0): Pending...
  • Installing packaging (21.0): Skipped for the following reason: Already installed
  • Installing pluggy (1.0.0): Pending...
  • Installing pluggy (1.0.0): Skipped for the following reason: Already installed
  • Installing py (1.10.0): Pending...
  • Installing py (1.10.0): Skipped for the following reason: Already installed
  • Installing python-dateutil (2.8.2): Pending...
  • Installing python-dateutil (2.8.2): Skipped for the following reason: Already installed
  • Installing pytz (2021.1): Pending...
  • Installing pytz (2021.1): Skipped for the following reason: Already installed
  • Installing toml (0.10.2): Pending...
  • Installing toml (0.10.2): Skipped for the following reason: Already installed
  • Installing cython (0.29.24): Pending...
  • Installing cython (0.29.24): Skipped for the following reason: Already installed
  • Installing pandas (0.25.3): Pending...
  • Installing pandas (0.25.3): Skipped for the following reason: Already installed
  • Installing pytest (6.2.5): Pending...
  • Installing pytest (6.2.5): Skipped for the following reason: Already installed

Installing the current project: <...>
```

It appears that it first removes the packages, and then tries to install the same packages but decides to skip as it thinks they are already installed, while in fact it just removed them. It shouldn't remove these packages in the first place.

The only workaround I can think of for now would be to stop using `--remove-untracked` option.

Thanks.
