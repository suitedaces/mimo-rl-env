pip >=19.2 cannot install packages via custom URLs with "one element" auth
**Environment**

* pip version: >= 19.2
* Python version: 2.7.10 and 3.7.2
* OS: macOS Mojave

<!-- Feel free to add more information about your environment here -->

**Description**
<!-- A clear and concise description of what the bug is. -->
When trying to install a package from a custom URL that requires authentication (e.g. from GitHub private repo releases), pip doesn't properly handle parsing of "one element" auth info e.g. GitHub access tokens (i.e. without `:` like the usual `user:password` auth info).

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
I want to be able to install my package from a private GitHub repo with an Auth Token like this:
```
pip install https://myaccesstoken@github.com/myorganization/myprivaterepo/archive/myrelease.zip#egg=mypackage
```
this works fine with `pip==19.1.1`

**How to Reproduce**
<!-- Describe the steps to reproduce this bug. -->

1. Create a private repo on GitHub with one release (can be empty).
2. Create an access token at https://github.com/settings/tokens/new for private repos
3. Try to install that release package (.zip) using the created token with `pip>=19.2` like in the section above.

The output should mention a successful *download* of the package and a "`setup.py` not found" error message (if the release was empty).

**Workaround**

As a workaround one can put `:` before or after the access token so the URL looks like:
```
https://:myaccesstoken@github.com/...
```

**Output**
Instead of installing the package, pip fails with "ERROR: HTTP error 404 while getting https://...".

I've created an empty private repo, with an empty release to test that. The output for `pip install -vvv ...` can be found here:
- [for pip 19.2](http://dpaste.com/2XGKP51),
- [for pip 19.1.1](http://dpaste.com/1EZ7JQW) (with expected `setup.py` not found error).

The issue/difference can be observed around `Starting new HTTPS connection (1): github.com:443`.

**Cause**
I've run a `git bisect` session for this issue and it pointed to this commit c63ee61027fe

This issue was also discussed at https://github.com/pypa/pip/issues/6775 (see https://github.com/pypa/pip/issues/6775#issuecomment-514284653 and https://github.com/pypa/pip/issues/6775#issuecomment-514299653).
