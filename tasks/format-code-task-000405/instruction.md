Webserver doesn't mask rendered fields for pending tasks
### Apache Airflow version

2.2.5 (latest released)

### What happened

When triggering a new dagrun the webserver will not mask secrets in the rendered fields for that dagrun's tasks which didn't start yet.

Tasks which have completed or are in state running are not affected by this.

### What you think should happen instead

The webserver should mask all secrets for tasks which have started or not started.

<img width="628" alt="Screenshot 2022-04-04 at 15 36 29" src="https://user-images.githubusercontent.com/7921017/161628806-c2c579e2-faea-40cc-835c-ac6802d15dc1.png">
.

### How to reproduce

Create a variable `my_secret` and run this DAG

```python
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.utils.dates import days_ago

with DAG(
    "secrets",
    start_date=days_ago(1),
    schedule_interval=None,
) as dag:
    wait = TimeDeltaSensor(
        task_id="wait",
        delta=timedelta(minutes=1),
    )

    task = wait >> BashOperator(
        task_id="secret_task",
        bash_command="echo '{{ var.value.my_secret }}'",
    )
```

While the first task `wait` is running, displaying rendered fields for the second task `secret_task` will show the unmasked secret variable.

<img width="1221" alt="Screenshot 2022-04-04 at 15 33 43" src="https://user-images.githubusercontent.com/7921017/161628734-b7b13190-a3fe-4898-8fa9-ff7537245c1c.png">



### Operating System

Debian (Astronomer Airflow Docker image)

### Versions of Apache Airflow Providers

```
apache-airflow-providers-amazon==1!3.2.0
apache-airflow-providers-cncf-kubernetes==1!3.0.0
apache-airflow-providers-elasticsearch==1!3.0.2
apache-airflow-providers-ftp==1!2.1.2
apache-airflow-providers-google==1!6.7.0
apache-airflow-providers-http==1!2.1.2
apache-airflow-providers-imap==1!2.2.3
apache-airflow-providers-microsoft-azure==1!3.7.2
apache-airflow-providers-mysql==1!2.2.3
apache-airflow-providers-postgres==1!4.1.0
apache-airflow-providers-redis==1!2.0.4
apache-airflow-providers-slack==1!4.2.3
apache-airflow-providers-sqlite==1!2.1.3
apache-airflow-providers-ssh==1!2.4.3
```

### Deployment

Astronomer

### Deployment details

_No response_

### Anything else

We have seen this issue also in Airflow 2.2.3.

### Are you willing to submit PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
