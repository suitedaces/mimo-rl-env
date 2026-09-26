# Problem Statement

When I do a clean `pip install salt` on newer Python, it doesn’t pull in `distro`, and then Linux distro detection is broken unless I install it myself. Can Salt just include that dependency by default? Also, on Windows with Python 3.8, the install keeps trying to use the old `pymssql` pin and that seems to fail, so it’d be nice if that didn’t get selected there.

# Expected outcomes

- Base installation dependencies:
  - A normal/base Salt dependency install includes the `distro` package so it is available without users installing it separately.
  - The base dependency list no longer declares the obsolete `singledispatch==3.4.0.3` backport.

- Packaged and static dependency sets:
  - Platform/package requirement sets that pin dependencies include `distro==1.5.0` for current Salt packaging.
  - Windows pinned requirement sets use the same `distro==1.5.0` pin as the other packaged/static requirement sets.

- Windows Python version handling:
  - Windows dependency resolution does not select the old pinned `pymssql` dependency on Python 3.8 or newer.
  - Windows dependency resolution still permits the existing pinned `pymssql==2.1.4` dependency for Python versions older than 3.8.

# Implementation notes

- The concrete files and dependency-generation workflow should follow the repository’s existing packaging and requirements conventions.
- The exact mechanism for keeping generated/static requirement sets consistent is up to the implementation, as long as the externally visible dependency resolution behavior above is satisfied.
