Backwards-incompatible API change in OAuth2Validator in 1.6.0
**Describe the bug**

PR #967 changed the API for `OAuth2Validator.get_additional_claims` in a backwards-incompatible way (and the project major version has not been bumped, which would have been required by semantic versioning).

Specifically, the `request` argument was removed, which we relied upon downstream. It seems that the functionality has remained (in a slightly more complex way), but such breakage is not expected between minor versions.

I propose to revert the change in 1.6.1, and make a new release 2.0.0 introducing the breaking change.

**Expected behavior**

We expect the (documented) API not to break backwords-incompatibly in minor versions.

**Version**
1.6.0
