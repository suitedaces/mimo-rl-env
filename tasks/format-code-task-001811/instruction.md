Locust stuck in "Shape worker starting" when restarting a test from the webUI
When restarting a test (that uses LoadTestShape) from the webUI, the test gets stuck in "Shape worker starting" (until tick() signals another change in shape). 

#### Expected behavior
Test should start immediately without waiting on a change in load shape. 

#### Actual behavior
Test waits on a change in load shape

Example file: 
```
import datetime
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape

class UserTasks(TaskSet):
    @task
    def something(self):
        self.client.post(f'/')

class WebsiteUser(HttpUser):
    wait_time = constant(1)
    tasks = [UserTasks]

class upAndDown(LoadTestShape):
    def tick(self):
        if datetime.datetime.now().minute % 2 == 0:
            user_count = 4
        else:
            user_count = 5
        return (user_count, 2)
```
Start test then stop. Restart the test from webUI (New test). The test won't start running until the minute changes (and tick() returns a different user_count). 

Seems to be due to 
``` 
            elif self.shape_last_state == new_state:
                gevent.sleep(1)
```
in runners.py > Runner > shape_worker

and `self.shape_last_state = None` not being reset in stop()


- Python version: 3.6.9
- Locust version:  1.2.1
