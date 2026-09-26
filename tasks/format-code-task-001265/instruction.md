LOG_FILTER not working as it should?
Good evening folks,

I have a problem with LOG_FILTER. According to the docs, one can remove `TAG_SAVE_AS is set to False` by configuring `LOG_FILTER` this way:

```python
import logging
LOG_FILTER = [(logging.WARN, 'TAG_SAVE_AS is set to False')]
```

So to ignore `AUTHOR_SAVE_AS is set to False` and `CATEGORY_SAVE_AS is set to False`, it must be :

```python
import logging
LOG_FILTER = [
    (logging.WARN, 'AUTHOR_SAVE_AS is set to False'),
    (logging.WARN, 'CATEGORY_SAVE_AS is set to False')
]
```
Right?

So this is what I did:
```bash
$ head pelicanconf.py -n 20
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime
import logging

import pelican

PELICAN_VERSION = pelican.__version__

[...]

LOG_FILTER = [
    (logging.WARN, 'AUTHOR_SAVE_AS is set to False'),
    (logging.WARN, 'CATEGORY_SAVE_AS is set to False')
]

AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False
TAG_SAVE_AS = False
TAGS_SAVE_AS = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False
ARCHIVES_SAVE_AS = False

$ make publish
pelican /mnt/c/Users/max/Code/mlcdf/content -o /mnt/c/Users/max/Code/mlcdf/output -s /mnt/c/Users/max/Code/mlcdf/publishconf.py
WARNING: CATEGORY_SAVE_AS is set to False
WARNING: AUTHOR_SAVE_AS is set to False
Done: Processed 2 articles, 0 drafts, 4 pages, 1 hidden page and 0 draft pages in 0.52 seconds.
```
2 things here:
- it didn't work: `AUTHOR_SAVE_AS is set to False` and `CATEGORY_SAVE_AS is set to False` are still logged.
- and, you may have noticed that, despite setting `TAG_SAVE_AS = False`, and not filtering it, I did not see `TAG_SAVE_AS is set to False` in the logs.

Using the template to filter worked (but it will also filter out other logs matching the template which is not what you would necessary want):
```
import logging
LOG_FILTER = [
    (logging.WARN, '%s is set to %s'),
]
```

* Am I missing something?
* What's the intended behaviour here? Is there an actual bug in the code? Or is the code example in the docs just wrong?

I'm a bit lost. 🙃 

Maxime
