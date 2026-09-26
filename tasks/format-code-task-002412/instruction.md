"poetry init --dependency django" does nothing
<!--
  Hi there! Thank you for discovering and submitting an issue.

  Before you submit this; let's make sure of a few things.
  Please make sure the following boxes are ticked if they are correct.
  If not, please try and fulfill these first.
-->

<!-- Checked checkbox should look like this: [x] -->
- [x] I am on the [latest](https://github.com/sdispater/poetry/releases/latest) Poetry version.
- [x] I have searched the [issues](https://github.com/sdispater/poetry/issues) of this repo and believe that this is not a duplicate.
- [ ] If an exception occurs when executing a command, I executed it again in debug mode (`-vvv` option).

<!--
  Once those are done, if you're able to fill in the following list with your information,
  it'd be very helpful to whoever handles the issue.
-->

- **OS version and name**: Ubuntu Xenial
- **Poetry version**: o.12.10
- **Link of a [Gist](https://gist.github.com/) with the contents of your pyproject.toml file**: https://gist.github.com/nottrobin/dddb94232b2d79f089ea7ef3b3dab4a4

## Issue
<!-- Now feel free to write your issue, but please be descriptive! Thanks again 🙌 ❤️ -->

If I do:

``` bash
poetry init --dependency django
```

It walks me through the same guide as normal, and if when it asks if I went to define dependencies I select "no", then it doesn't add Django to `pyproject.toml` as a dependency, so `--dependency django` effectively did nothing.

It should either:

- Edit the guide to ask if you want to specify any *further* dependencies, and maybe indicate that it's going to install Django anyway; or
- Error saying "`--dependency` is only compatible with `--no-interaction`"
