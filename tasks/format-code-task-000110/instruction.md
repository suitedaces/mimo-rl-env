[apps.paint_annotations] Add option to filter iscrowd
The `iscrowd` attribute present in COCO annotations is currently being ignored and `crowd` boxes are being painted (the big purple sheep box):

![000000545959_result](https://user-images.githubusercontent.com/12677733/107704160-1b71e580-6cbd-11eb-9e56-e964b6e2aec9.jpg)

It would be nice to add an optional argument to filter out this annotations (possibly with default True).
