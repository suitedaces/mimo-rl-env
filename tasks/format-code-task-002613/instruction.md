## Add PHP 8 support

PHP 8.0 has been out for a while now, and I'd like to use Sculpin on a fresh setup where PHP 8 is the only available version.

Right now installation fails immediately:

```
$ composer require sculpin/sculpin
...
  Problem 1
    - sculpin/sculpin ... requires php ^7.2 -> your php version (8.0.x) does not satisfy that requirement.
```

If I force it with `--ignore-platform-reqs` just to see how far things get, the install completes but then running the binary doesn't get me a working build either — there are a few spots in the codebase that don't behave correctly under PHP 8 and the dev toolchain (phpunit etc.) is also pinned to versions that don't run on 8.

Could the project be updated so that Sculpin installs and runs on PHP 8? Keeping the recent 7.x line working would also be nice for people who haven't upgraded yet.
