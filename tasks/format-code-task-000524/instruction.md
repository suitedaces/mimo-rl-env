Appveyor badge shows internal error if there are no builds
When trying to get an Appveyor badge for a project that doesn't have any builds yet, shields generates an internal error:
![ss1536772059-5026](https://user-images.githubusercontent.com/2406499/45441442-07a99b80-b68d-11e8-8e34-d847a3a61ac7.png)

Glancing at the service file, it queries their JSON API and extracts the build status from the `build.status` property - however for projects that have no builds the `build` property does not exist.
