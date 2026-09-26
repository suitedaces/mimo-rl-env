EODataAccessGateway constructor fails on AWS Lambda
**Describe the bug**

`makedirs` [invocation](https://github.com/CS-SI/eodag/blob/develop/eodag/api/core.py#L98) within the EODataAccessGateway constructor causes `OSError: [Errno 30] Read-only file system` when run on AWS Lambda

**Code To Reproduce**
CLI commands or Python code snippet to reproduce the bug. Please use maximum verbosity using:

```py
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from eodag import EODataAccessGateway

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):
    EODataAccessGateway()
```

**Output**
Compete output obtained with maximal verbosity.

```
[ERROR] OSError: [Errno 30] Read-only file system: '/home/sbx_user1051'
Traceback (most recent call last):
  File "/opt/python/aws_lambda_powertools/tracing/tracer.py", line 305, in decorate
    response = lambda_handler(event, context, **kwargs)
  File "/opt/python/aws_lambda_powertools/logging/logger.py", line 438, in decorate
    return lambda_handler(event, context, *args, **kwargs)
  File "/var/task/<my file, my line>, in lambda_handler
    EODataAccessGateway()
  File "/opt/python/eodag/api/core.py", line 91, in __init__
    makedirs(self.conf_dir)
  File "/opt/python/eodag/utils/__init__.py", line 496, in makedirs
    os.makedirs(dirpath)
  File "/var/lang/lib/python3.9/os.py", line 215, in makedirs
    makedirs(head, exist_ok=exist_ok)
  File "/var/lang/lib/python3.9/os.py", line 215, in makedirs
    makedirs(head, exist_ok=exist_ok)
  File "/var/lang/lib/python3.9/os.py", line 225, in makedirs
    mkdir(name, mode)
```

**Environment:**

 - Python version: 3.9
 - EODAG version: 2.5.2
 - Runtime: AWS Lambda

**Additional context**

File system on AWS Lambda is read-only. It has "ephemeral storage" that could be accessed in `/tmp` ([1](https://aws.amazon.com/blogs/aws/aws-lambda-now-supports-up-to-10-gb-ephemeral-storage/), [2](https://aws.amazon.com/blogs/aws/aws-lambda-now-supports-up-to-10-gb-ephemeral-storage/)), however this class does not accept any configuration to where to point to `makedirs`. 

The workaround that heavily relies on the [current implementation](https://github.com/CS-SI/eodag/blob/develop/eodag/api/core.py#L97) is to change `$HOME` env var before invoking the constructor. But it is barely acceptable and extremely inconvenient, since this variable is used by many tools locally and in automated tools along the way.
