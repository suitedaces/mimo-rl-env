**Describe your environment**
- opentelemetry-exporter-prometheus==1.12.0rc1
- opentelemetry-sdk==1.19.0
- opentelemetry-api==1.19.0
- Python 3.11.0

**Steps to reproduce**
```python
from opentelemetry import metrics

test_counter = metrics.get_meter("module").create_counter('test_counter', description='counter used for testing')

test_counter.add(1, {'location': 'here', 'source': 'external'})
test_counter.add(1, {'source': 'internal', 'reason': 'error'})
```

**What is the expected behavior?**
I expect labels to be the ones specified. But it seems like it only looks at the last call to `counter.add` to figure out label names, and then just looks at the position of the labels. I also expect these the be the same metric. (no duplicate HELP, TYPE). This also has other weird behaviour when the dict size is different.

The otlp api for counter says this: `Users can provide attributes to associate with the increment value, but it is up to their discretion. Therefore, this API MUST be structured to accept a variable number of attributes, including none.` This suggest to me that it should be possible to set only certain labels (as far as I understand prometheus also supports missing labels). If this is not the case it should probably be made possible to define label names when creating a counter so this can at least by static type checked. This would also be helpful if missing labels are supported to prevent typos when specifying labels, but that should be probably a separate issue?

**What is the actual behavior?**
```
# HELP test_counter_total counter used for testing
# TYPE test_counter_total counter
test_counter_total{reason="external",source="here"} 1.0
# HELP test_counter_total counter used for testing
# TYPE test_counter_total counter
test_counter_total{reason="error",source="internal"} 1.0
```

### Describe your environment

```
[packages]
opentelemetry-distro = "==0.49b2"
opentelemetry-exporter-otlp = "==1.28.2"
opentelemetry-exporter-prometheus = "==0.49b2"
opentelemetry-instrumentation-asgi = "==0.49b2"
opentelemetry-instrumentation-fastapi = "==0.49b2"
opentelemetry-instrumentation-httpx = "==0.49b2"
opentelemetry-instrumentation-jinja2 = "==0.49b2"
opentelemetry-instrumentation-logging = "==0.49b2"
opentelemetry-instrumentation-urllib = "==0.49b2"
opentelemetry-instrumentation-urllib3 = "==0.49b2"
opentelemetry-instrumentation-aiohttp-client = "==0.49b2"
fastapi = "*"
uvicorn = {extras = ["standard"]}
```

### What happened?

The labels being assigned to the generated metrics, are wrong/out of order.

### Steps to Reproduce

MVC: https://github.com/jseiser/otlp_fastapi_repl/tree/main

### Expected Result

Correct metric labels

### Actual Result

1. Start the app

```
pipenv run opentelemetry-instrument uvicorn ui.main:app --proxy-headers --host=0.0.0.0 --port=5000 --log-level=error
Loading .env environment variables..
```

2. Check Metrics - makes sense, no traffic has happened
```
 curl http://localhost:9464/metrics 
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 2258.0
python_gc_objects_collected_total{generation="1"} 2915.0
python_gc_objects_collected_total{generation="2"} 60.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 170.0
python_gc_collections_total{generation="1"} 15.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="10",version="3.11.10"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 4.3268096e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 7.2364032e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.73869183682e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.66
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 18.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
```

3.  Hit Site once
```
curl http://localhost:5000         
{"message":"Hello World"}
```
4. Check Metrics - Looks Good - note http_target, and not_host_port.
```
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:5000",http_method="GET",http_scheme="http",http_server_name="localhost:5000",http_status_code="200",http_target="/",le="0.0",net_host_port="5000"} 0.0

http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:5000",http_method="GET",http_scheme="http",http_server_name="localhost:5000",http_status_code="200",http_target="/",le="0.0",net_host_port="5000"} 0.0
```

5. Hit site a few more times
```
curl http://localhost:5000         
{"message":"Hello World"}% 
curl http://localhost:5000         
{"message":"Hello World"}% 
```

6. Check Metrics - still good
7. Hit something else
```
curl http://localhost:5000/fakepath
{"detail":"Not Found"}
```

8. Check Metrics - Broken
```
http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:5000",http_method="GET",http_scheme="http",http_server_name="localhost:5000",http_status_code="200",le="0.0",net_host_port="/"} 5.0                           

http_server_duration_milliseconds_bucket{http_flavor="1.1",http_host="127.0.0.1:5000",http_method="GET",http_scheme="http",http_server_name="localhost:5000",http_status_code="404",le="0.0",net_host_port="5000"} 1.0

http_server_response_size_bytes_bucket{http_flavor="1.1",http_host="127.0.0.1:5000",http_method="GET",http_scheme="http",http_server_name="localhost:5000",http_status_code="404",le="0.0",net_host_port="5000"} 0.0
```


### Additional context

_No response_

### Would you like to implement a fix?

None
