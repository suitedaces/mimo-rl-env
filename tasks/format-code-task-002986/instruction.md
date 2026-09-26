Not downloading selenium patch versions successfully
## Expected Behavior
A new selenium server patch version should be downloaded with success.

## Current Behavior
When trying to download a new (_patch_) version of selenium server, a 404 is returned.

## Steps to Reproduce
Just try to download the new _4.1.1_ version of selenium.

## Logs
I think the issue is related to the way the download URL is built.
So, right now we have patch versions deployed under its minor version path:
https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.1.0/selenium-server-4.1.1.jar

So, a URL like https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.1.1/selenium-server-4.1.1.jar will fail with 404 not found.

## Your Environment
* Version of `selenium-standalone` that you are using: `8.0.3`
* Is there another tool calling `selenium-standalone` on your behalf: `@wdio/selenium-standalone-service@7.16.6`
* System/platform: macOS
* Other details that might be important: `Node v12.22.7`
