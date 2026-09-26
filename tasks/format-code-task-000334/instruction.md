pypa/pip#10909 is so far the "highest profile" discussion I've found on this topic.

It seems that [pip](https://github.com/pypa/pip) and [colorama](https://github.com/tartley/colorama) are going to support only `FORCE_COLOR=<anything>` and `NO_COLOR=<anything>`, but not `PY_COLORS`.

On the other hand, Pytest does support `PY_COLORS={1|0}` and `NO_COLOR=<anything>` (with `PY_COLORS` taking precedence).

So in the end it may be best to do the same as Pytest:
- `PY_COLORS={1|0}` (taking precedence over other options)
- `NO_COLOR=<anything>`
- and possibly `FORCE_COLOR=<anything>` (similar to [pip](https://github.com/pypa/pip) and [colorama](https://github.com/tartley/colorama))

As for the `true`/`false` discussion, I'm going to make the call to only support `PY_COLORS={0|1}` for now. Thanks @MatthijsBurgh for initiating the discussion and motivating me to look further into the topic!

_Originally posted by @akaihola in https://github.com/akaihola/darker/pull/353#discussion_r846752942_
