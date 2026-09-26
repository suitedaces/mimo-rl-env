## Custom subclass of `ImagesPipeline` ignores `IMAGES_*` settings

I have a custom image pipeline that extends `ImagesPipeline` to add some
project-specific behaviour:

```python
# myproject/pipelines.py
from scrapy.pipelines.images import ImagesPipeline

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # ... custom logic ...
        return super().get_media_requests(item, info)
```

In `settings.py` I enable it and configure the standard image settings:

```python
ITEM_PIPELINES = {
    'myproject.pipelines.MyImagesPipeline': 1,
}

IMAGES_STORE = '/tmp/images'
IMAGES_THUMBS = {
    'small': (50, 50),
    'big':   (270, 270),
}
IMAGES_MIN_WIDTH = 100
IMAGES_MIN_HEIGHT = 100
```

When I run the spider, none of these settings seem to take effect for my
subclass:

- no thumbnails get generated (default `THUMBS = {}` behaviour),
- the min-width / min-height filtering doesn't kick in,
- the expiration behaves like the hard-coded default.

If I swap `MyImagesPipeline` out for the stock `ImagesPipeline` in
`ITEM_PIPELINES`, the exact same `settings.py` works as expected:
thumbnails are produced and the size filtering kicks in.

So it looks like subclassing the pipeline silently disables the standard
`IMAGES_*` settings, and the user has no obvious way (from the docs) to
make them apply to their own subclass. I would expect a subclass to
inherit the default settings of its parent pipeline unless I explicitly
override them for that subclass.

Same issue presumably applies to subclasses of `FilesPipeline` and the
`FILES_*` settings.
