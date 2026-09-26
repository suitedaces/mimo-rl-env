[Custom builder] $IMAGES is always a single image
We currently pass the build script the `IMAGES` env variable. This variable contains the list of images to build. However, this variable always contains a single tag.

I think we should deprecate this value and use `IMAGE` instead.
