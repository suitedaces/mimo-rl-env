Scheduler is spending most of its time in clear_not_launched_queued_tasks function
### Apache Airflow version

2.7.1

### What happened

Airflow running the clear_not_launched_queued_tasks function on a certain frequency (default 30 seconds). When we run the airflow on a large Kube cluster (pods more than > 5K).  Internally the clear_not_launched_queued_tasks function loops through each queued task and checks the corresponding worker pod existence in the Kube cluster. Right this existence check using list pods Kube API. The API is taking more than 1s. if there are 120 queued tasks, then it will take ~ 120 seconds (1s * 120). So, this leads the scheduler to spend most of its time in this function rather than scheduling the tasks. It leads to none of the jobs being scheduled or degraded scheduler performance.

### What you think should happen instead

It would be nice to get all the airflow worker pods in a one/few batch calls rather than for each task. These batch calls helps to speed the processing of clear_not_launched_queued_tasks function call. 

### How to reproduce

Run the airflow on large Kube clusters (> 5K pods). Simulate the airflow to run the 100 parallel DAG runs for every minute. 

### Operating System

Cent OS 7

### Versions of Apache Airflow Providers

2.3.3, 2.7.1

### Deployment

Other Docker-based deployment

### Deployment details

Terraform based airflow deployment

### Anything else

_No response_

### Are you willing to submit PR?

- [x] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
