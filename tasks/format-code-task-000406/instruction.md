AttributeError: 'CeleryKubernetesExecutor' object has no attribute 'send_callback'
### Apache Airflow version

2.3.0 (latest released)

### What happened

The issue started to occur after upgrading airflow from v2.2.5 to v2.3.0. The schedulers are crashing when DAG's SLA is configured. Only occurred when I used `CeleryKubernetesExecutor`. Tested on `CeleryExecutor` and it works as expected.

```
Traceback (most recent call last):                                                                                                     
  File "/home/airflow/.local/bin/airflow", line 8, in <module>                                                                         
    sys.exit(main())                                                                                                                   
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/__main__.py", line 38, in main                                        
    args.func(args)                                                                                                                    
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/cli/cli_parser.py", line 51, in command                               
    return func(*args, **kwargs)                                                                                                       
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/utils/cli.py", line 99, in wrapper                                    
    return f(*args, **kwargs)                                                                                                          
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/cli/commands/scheduler_command.py", line 75, in scheduler             
    _run_scheduler_job(args=args)                                                                                                      
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/cli/commands/scheduler_command.py", line 46, in _run_scheduler_job    
    job.run()                                                                                                                          
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/jobs/base_job.py", line 244, in run                                   
    self._execute()                                                                                                                    
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/jobs/scheduler_job.py", line 736, in _execute                         
    self._run_scheduler_loop()                                                                                                         
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/jobs/scheduler_job.py", line 824, in _run_scheduler_loop              
    num_queued_tis = self._do_scheduling(session)                                                                                      
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/jobs/scheduler_job.py", line 919, in _do_scheduling                   
    self._send_dag_callbacks_to_processor(dag, callback_to_run)                                                                        
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/jobs/scheduler_job.py", line 1179, in _send_dag_callbacks_to_processor
    self._send_sla_callbacks_to_processor(dag)                                                                                         
  File "/home/airflow/.local/lib/python3.9/site-packages/airflow/jobs/scheduler_job.py", line 1195, in _send_sla_callbacks_to_processor
    self.executor.send_callback(request)                                                                                               
AttributeError: 'CeleryKubernetesExecutor' object has no attribute 'send_callback'
```

### What you think should happen instead

Work like previous version

### How to reproduce

1. Use `CeleryKubernetesExecutor`
2. Configure DAG's SLA

DAG to reproduce:
```
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Example DAG demonstrating the usage of the BashOperator."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

DEFAULT_ARGS = {
    "sla": timedelta(hours=1),
}

with DAG(
    dag_id="example_bash_operator",
    default_args=DEFAULT_ARGS,
    schedule_interval="0 0 * * *",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
) as dag:
    run_this_last = DummyOperator(
        task_id="run_this_last",
    )

    # [START howto_operator_bash]
    run_this = BashOperator(
        task_id="run_after_loop",
        bash_command="echo 1",
    )
    # [END howto_operator_bash]

    run_this >> run_this_last

    for i in range(3):
        task = BashOperator(
            task_id="runme_" + str(i),
            bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        )
        task >> run_this

    # [START howto_operator_bash_template]
    also_run_this = BashOperator(
        task_id="also_run_this",
        bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    )
    # [END howto_operator_bash_template]
    also_run_this >> run_this_last

# [START howto_operator_bash_skip]
this_will_skip = BashOperator(
    task_id="this_will_skip",
    bash_command='echo "hello world"; exit 99;',
    dag=dag,
)
# [END howto_operator_bash_skip]
this_will_skip >> run_this_last

if __name__ == "__main__":
    dag.cli()

```

### Operating System

Debian GNU/Linux 11 (bullseye)

### Versions of Apache Airflow Providers

_No response_

### Deployment

Official Apache Airflow Helm Chart

### Deployment details

_No response_

### Anything else

_No response_

### Are you willing to submit PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
