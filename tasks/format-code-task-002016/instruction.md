Label contour values < 0 act the same as 0
## 🐛 Bug

Label contour values that are < 0 act the same as contour value of 0, ie. the whole label is filled in.

## To Reproduce

1. Create a labels layer with some labels
2. Use the GUI to set the contour value to < 0

<!-- If you have a code sample, error messages, stack traces, please provide it here as well -->

## Expected behavior
Values < 0 cannot be selected.

## Environment
Current `napari` main branch

## Additional context

Sort of related to https://github.com/napari/napari/issues/5798, which will also require limiting the allowed valeus for contour.
