run_job_template removes relative path from controller URL
### Please confirm the following

- [X] I agree to follow this project's [code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
- [X] I have checked the [current issues](https://github.com/ansible/ansible-rulebook/issues) for duplicates.
- [X] I understand that ansible-rulebook is open source software provided for free and that I might not receive a timely response.

### Bug Summary

When specifying a URL with a relative path to the controller (AWX), the API call is sent to the absolute path /api/v2.

Configured eda.yml:

```
$ cat eda.yaml 
# eda.yaml
apiVersion: eda.ansible.com/v1alpha1
kind: EDA
metadata:
  name: my-eda
spec:
  automation_server_url: http://awx-demo-service.awx/awx/
  service_type: ClusterIP
  ingress_type: ingress
```

Here's the output of the rulebook activation:

```
2024-01-19 23:32:13,505 - ansible_rulebook.websocket - INFO - websocket ws://my-eda-daphne:8001/api/eda/ws/ansible-rulebook connected
2024-01-19 23:32:13,552 - ansible_rulebook.job_template_runner - INFO - Attempting to connect to Controller http://awx-demo-service.awx/awx
2024-01-19 23:32:13,553 - ansible_rulebook.job_template_runner - ERROR - Error connecting to controller 404, message='Not Found', url=URL('http://awx-demo-service.awx/api/v2/config/')
2024-01-19 23:32:13,554 - ansible_rulebook.cli - ERROR - Terminating 404, message='Not Found', url=URL('http://awx-demo-service.awx/api/v2/config/') 
```

After removing the leading "/" from UNIFIED_TEMPLATE_SLUG and CONFIG_SLUG. It started to work locally for me.



### Environment

eda-server-operator 2.10.0 with quay.io/ansible/ansible-rulebook:v1.0.4

### Steps to reproduce

You'll need AWX installed on a different path than '/`.

I installed ansible-rulebook from brew (OSX).

Export the following variable (CLI options or documentation didn't work).

```
export EDA_CONTROLLER_URL="http://localhost:8081/awx/"
export EDA_CONTROLLER_TOKEN="ZesMMFepb2WYfHNEfvv1pMz0PMbUkE"
```

Start a simple rulebook using job_run_template.
Verify it doesn't connect.

My output looked like this on ansible-rulebook ran locally:

```
$ ansible-rulebook -r rulebooks/hello.yaml -vv 
2024-01-19 20:02:55,303 - asyncio - DEBUG - Using selector: KqueueSelector
2024-01-19 20:02:55,304 - ansible_rulebook.app - DEBUG - Loading rules from the file system rulebooks/hello.yaml
2024-01-19 20:02:55,309 - ansible_rulebook.condition_parser - DEBUG - [Identifier(value='event.i'), '==', Integer(value=1)]
2024-01-19 20:02:55,309 - ansible_rulebook.job_template_runner - INFO - Attempting to connect to Controller http://localhost:8081/awx/
2024-01-19 20:02:55,317 - ansible_rulebook.cli - ERROR - Terminating Expecting value: line 1 column 1 (char 0)
```

Once I remove the trailing slash (there is a different error):

```
$ ansible-rulebook -r rulebooks/hello.yaml -vv 
2024-01-19 20:16:46,145 - asyncio - DEBUG - Using selector: KqueueSelector
2024-01-19 20:16:46,145 - ansible_rulebook.app - DEBUG - Loading rules from the file system rulebooks/hello.yaml
2024-01-19 20:16:46,150 - ansible_rulebook.condition_parser - DEBUG - [Identifier(value='event.i'), '==', Integer(value=1)]
2024-01-19 20:16:46,151 - ansible_rulebook.job_template_runner - INFO - Attempting to connect to Controller http://localhost:8081/awx/
2024-01-19 20:16:46,259 - ansible_rulebook.app - INFO - AAP Version 23.6.0
2024-01-19 20:16:46,259 - ansible_rulebook.app - INFO - Starting sources
2024-01-19 20:16:46,259 - ansible_rulebook.app - INFO - Starting rules
2024-01-19 20:16:46,259 - ansible_rulebook.engine - INFO - run_ruleset
2024-01-19 20:16:46,260 - drools.ruleset - INFO - Using jar: /opt/homebrew/lib/python3.9/site-packages/drools/jars/drools-ansible-rulebook-integration-runtime-1.0.5-SNAPSHOT.jar
2024-01-19 20:16:46,508 - drools.ruleset - DEBUG - Creating Drools Ruleset
2024-01-19 20:16:46 801 [main] INFO org.drools.ansible.rulebook.integration.api.rulesengine.AbstractRulesEvaluator - Start automatic pseudo clock with a tick every 100 milliseconds
2024-01-19 20:16:46,805 - drools.ruleset - DEBUG - Ruleset Session ID : 1
2024-01-19 20:16:46,805 - ansible_rulebook.engine - INFO - ruleset define: {"name": "Hello Events", "hosts": ["localhost"], "sources": [{"EventSource": {"name": "ansible.eda.range", "source_name": "ansible.eda.range", "source_args": {"limit": 5}, "source_filters": []}}], "rules": [{"Rule": {"name": "Say Hello", "condition": {"AllCondition": [{"EqualsExpression": {"lhs": {"Event": "i"}, "rhs": {"Integer": 1}}}]}, "actions": [{"Action": {"action": "run_job_template", "action_args": {"name": "Hello World", "organization": "Default"}}}], "enabled": true}}]}
2024-01-19 20:16:46,805 - drools.dispatch - DEBUG - Establishing async channel
2024-01-19 20:16:46,817 - ansible_rulebook.engine - INFO - load source
2024-01-19 20:16:47,077 - ansible_rulebook.engine - ERROR - Source error Could not find source plugin for ansible.eda.range
2024-01-19 20:16:47,077 - ansible_rulebook.engine - ERROR - Shutting down source: ansible.eda.range error : Could not find source plugin for ansible.eda.range
```


### Actual results

404 error due to improper path

### Expected results

Expecting the api call to use the base url.

### Additional information

This was difficult enough to bring up as a server (EDA Controller + AWX). 

Because I needed to have AWX and EDA on the same port, I had to configured AWX on the `/awx` router which is supported by the operator.

```
$ cat awx-demo.yml 
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-demo
spec:
  service_type: nodeport
  ingress_type: ingress
  ingress_path: /awx
```

Code to reproduce the issue in the code:

```
>>> from urllib.parse import urljoin
>>> UNIFIED_TEMPLATE_SLUG = "/api/v2/unified_job_templates/"
>>> CONFIG_SLUG = "/api/v2/config/"
>>> host="http://awx-demo-service/awx"
>>> url = urljoin(host, href_slug)
>>> url = urljoin(host, CONFIG_SLUG)
>>> print(url)
http://awx-demo-service/api/v2/config/
```
^^^ Incorrect

Removing the "/" in CONFIG_SLUG:

```
>>> CONFIG_SLUG = "api/v2/config/"
>>> print(urljoin(host, CONFIG_SLUG))
http://awx-demo-service/awx/api/v2/config/
```
