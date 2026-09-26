Breaking change in python-i3ipc breaks i3 listers
A relatively recent, major update in i3ipc (`v2.0.1`) breaks some of our segments and listers here.
I discovered it today while updating all my python packages (for python 3.8).

In essence, the python class wrappers around i3ipc JSON responses that our code deals with have changed, so that `reply['attr']` is no longer valid, and `reply.attr` or `getattr(reply, 'attr')` must be used.
This is relevant in powerline/listers/i3wm.py and powerline/segments/i3wm.py.
