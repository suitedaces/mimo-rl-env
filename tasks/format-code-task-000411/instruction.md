Make `webserver_config.py` location customizable
**Description**
`webserver_config.py` location is [hard-coded](https://github.com/apache/airflow/blob/c2db0dfeb13ee679bf4d7b57874f0fcb39c0f0ed/airflow/configuration.py#L769) as follows:
```
WEBSERVER_CONFIG = AIRFLOW_HOME + '/webserver_config.py'
```
It would be great if this path is customizable.

**Use case / motivation**
Since `AIRFLOW_HOME/config` is already in `PYTHONPATH` (though that's also hard-coded), it's common for user to mount all config files under `AIRFLOW_HOME/config`.  However, this `webserver_config.py` needs extra handling, either by mounting using a `subPath` explicitly, or in my case, creating a symbolic link from `AIRFLOW_HOME/webserver_config.py` to `AIRFLOW_HOME/config/webserver_config.py` in the image.
