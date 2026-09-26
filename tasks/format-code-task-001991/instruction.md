Run an extension in a linked profile for persistence
Calling [run --firefox-profile=myprofile](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/web-ext_command_reference#web-ext_run) will copy a custom profile into a temporary profile. It will not affect the original profile. This new feature is to run the extension directly in the custom profile so that any profile changes will be saved. 

Example use case: if you're developing an extension that has a splash screen on install, you may not want to see that screen every time you launch Firefox to test it.

We should probably introduce a new option that can be called alongside the existing ones like this:
````bash
web-ext run --firefox-profile=myprofile --keep-profile-changes
````
