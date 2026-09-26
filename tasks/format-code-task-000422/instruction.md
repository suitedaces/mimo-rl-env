cordova plugin rm fails when multiple asset elements add content to plugins/<plugin-id> folder
# Bug Report

## Problem
If a plugin's plugin.xml file contains multiple `asset `elements which add content to the `plugins/<plugin-id>` folder the operation `cordova plugin rm <plugin-id>` fails with message:

```
Error during processing of action! Attempting to revert...
TypeError [ERR_INVALID_ARG_TYPE]: The "code" argument must be of type number. Received type string ('ENOENT')
    at process.set [as exitCode] (node:internal/bootstrap/node:123:9)
    at /Users/CDM/desb1224/cordova/cordova-12.0.0/node_modules/cordova/bin/cordova:32:22
```

### What is expected to happen?
The operation should be removed completely.


### What does actually happen?
The plugin is not completely removed.



## Information
<!-- Include all relevant information that might help understand and reproduce the problem -->
The problem is caused by code in the method `asset.uninstall` in `\cordova-ios\lib\plugman\pluginHandlers.js`.  After removing the asset file another call is made to `removeFileF `to remove the plugin folder:
```
  removeFileF(path.resolve(project.www, 'plugins', plugin.id));
  ...

function removeFileF (file) {
    fs.rmSync(file, { recursive: true, force: true });
}
```
The recursive call in `removeFileF` deletes any other assets sharing the same path, and on attempting to delete those assets the operation fails with the error given above

The plugin can be removed if ios platform is removed first.

This error is related to changes in made to resolve issue [https://github.com/apache/cordova-ios/issues/1443](https://github.com/apache/cordova-ios/issues/1443):
[https://github.com/apache/cordova-ios/pull/1446/files](https://github.com/apache/cordova-ios/pull/1446/files)


### Command or Code
<!-- What command or code is needed to reproduce the problem? -->
Add a plugin containing multiple assets in the same folder, for example with something along the following lines in plugin.xml:
```
	<asset src="www/js/mycode/mycode1.js" target="plugins/my-plugin-id/www/js/mycode/mycode1"/>
	<asset src="www/js/mycode/mycode2.js" target="plugins/my-plugin-id/www/js/mycode/mycode2"/>
```
Attempting to remove the plugin (when ios platform is installed) shoudl trigger the error.


### Environment, Platform, Device
<!-- In what environment, on what platform or on which device are you experiencing the issue? -->
Error occurs on development machine.

### Version information
<!-- 
What are relevant versions you are using?
For example:
Cordova: Cordova CLI, Cordova Platforms, Cordova Plugins 
Other Frameworks: Ionic Framework and CLI version
Operating System, Android Studio, Xcode etc.
-->
- Cordova 12.0.0
- cordova-ios 7.1.1



## Checklist
<!-- Please check the boxes by putting an x in the [ ] like so: [x] -->

- [X] I searched for existing GitHub issues
- [X] I updated all Cordova tooling to most recent version
- [X] I included all the necessary information above
