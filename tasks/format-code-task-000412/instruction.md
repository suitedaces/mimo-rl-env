Deserialization of old xcom data fails after upgrade to 2.6.1 from 2.5.2 when calling /xcom/list/ [GET]
### Apache Airflow version

2.6.1

### What happened

After upgrading from airflow 2.5.2 to 2.6.1 calling the endpoint `xcom/list/` we get the following exception:
```
[2023-06-07T12:16:50.050+0000] {app.py:1744} ERROR - Exception on /xcom/list/ [GET]
Traceback (most recent call last):
  File "/home/airflow/.local/lib/python3.10/site-packages/flask/app.py", line 2529, in wsgi_app
    response = self.full_dispatch_request()
  File "/home/airflow/.local/lib/python3.10/site-packages/flask/app.py", line 1825, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/home/airflow/.local/lib/python3.10/site-packages/flask/app.py", line 1823, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/airflow/.local/lib/python3.10/site-packages/flask/app.py", line 1799, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/home/airflow/.local/lib/python3.10/site-packages/flask_appbuilder/security/decorators.py", line 139, in wraps
    return f(self, *args, **kwargs)
  File "/home/airflow/.local/lib/python3.10/site-packages/flask_appbuilder/views.py", line 554, in list
    widgets = self._list()
  File "/home/airflow/.local/lib/python3.10/site-packages/flask_appbuilder/baseviews.py", line 1177, in _list
    widgets = self._get_list_widget(
  File "/home/airflow/.local/lib/python3.10/site-packages/flask_appbuilder/baseviews.py", line 1076, in _get_list_widget
    count, lst = self.datamodel.query(
  File "/home/airflow/.local/lib/python3.10/site-packages/flask_appbuilder/models/sqla/interface.py", line 500, in query
    query_results = query.all()
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/orm/query.py", line 2773, in all
    return self._iter().all()
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 1476, in all
    return self._allrows()
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 401, in _allrows
    rows = self._fetchall_impl()
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 1389, in _fetchall_impl
    return self._real_result._fetchall_impl()
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/engine/result.py", line 1813, in _fetchall_impl
    return list(self.iterator)
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/orm/loading.py", line 151, in chunks
    rows = [proc(row) for row in fetch]
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/orm/loading.py", line 151, in <listcomp>
    rows = [proc(row) for row in fetch]
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/orm/loading.py", line 984, in _instance
    state.manager.dispatch.load(state, context)
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/event/attr.py", line 334, in __call__
    fn(*args, **kw)
  File "/home/airflow/.local/lib/python3.10/site-packages/sqlalchemy/orm/mapper.py", line 3702, in _event_on_load
    instrumenting_mapper._reconstructor(state.obj())
  File "/home/airflow/.local/lib/python3.10/site-packages/airflow/models/xcom.py", line 128, in init_on_load
    self.value = self.orm_deserialize_value()
  File "/home/airflow/.local/lib/python3.10/site-packages/airflow/models/xcom.py", line 677, in orm_deserialize_value
    return BaseXCom._deserialize_value(self, True)
  File "/home/airflow/.local/lib/python3.10/site-packages/airflow/models/xcom.py", line 659, in _deserialize_value
    return json.loads(result.value.decode("UTF-8"), cls=XComDecoder, object_hook=object_hook)
  File "/usr/local/lib/python3.10/json/__init__.py", line 359, in loads
    return cls(**kw).decode(s)
  File "/usr/local/lib/python3.10/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/local/lib/python3.10/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
  File "/home/airflow/.local/lib/python3.10/site-packages/airflow/utils/json.py", line 126, in orm_object_hook
    return deserialize(dct, False)
  File "/home/airflow/.local/lib/python3.10/site-packages/airflow/serialization/serde.py", line 209, in deserialize
    o = _convert(o)
  File "/home/airflow/.local/lib/python3.10/site-packages/airflow/serialization/serde.py", line 273, in _convert
    return {CLASSNAME: old[OLD_TYPE], VERSION: DEFAULT_VERSION, DATA: old[OLD_DATA][OLD_DATA]}
KeyError: '__var'
```

Some xcom entries from previous airflow versions seem to be incompatible with the new refactored serialization from https://github.com/apache/airflow/pull/28067

### What you think should happen instead

xcom entries should be displayed

### How to reproduce
Add an entry to your the xcom table where value contains: 
` [{"__classname__": "airflow.datasets.Dataset", "__version__": 1, "__data__": {"__var": {"uri": "bq://google_cloud_default@?table=table_name&schema=schema_name", "extra": null}, "__type": "dict"}}]`

### Operating System

Debian GNU/Linux 11 (bullseye)

### Versions of Apache Airflow Providers

apache-airflow-providers-amazon==8.0.0
apache-airflow-providers-apache-kafka==1.1.0
apache-airflow-providers-celery==3.1.0
apache-airflow-providers-cncf-kubernetes==6.1.0
apache-airflow-providers-common-sql==1.4.0
apache-airflow-providers-docker==3.6.0
apache-airflow-providers-elasticsearch==4.4.0
apache-airflow-providers-ftp==3.3.1
apache-airflow-providers-google==10.1.1
apache-airflow-providers-grpc==3.1.0
apache-airflow-providers-hashicorp==3.3.1
apache-airflow-providers-http==4.3.0
apache-airflow-providers-imap==3.1.1
apache-airflow-providers-microsoft-azure==6.0.0
apache-airflow-providers-mysql==5.0.0
apache-airflow-providers-odbc==3.2.1
apache-airflow-providers-postgres==5.4.0
apache-airflow-providers-redis==3.1.0
apache-airflow-providers-sendgrid==3.1.0
apache-airflow-providers-sftp==4.2.4
apache-airflow-providers-slack==7.2.0
apache-airflow-providers-snowflake==4.0.5
apache-airflow-providers-sqlite==3.3.2
apache-airflow-providers-ssh==3.6.0

### Deployment

Other 3rd-party Helm chart

### Deployment details

_No response_

### Anything else

The double `old[OLD_DATA][OLD_DATA]` looks suspicious to me in  https://github.com/apache/airflow/blob/58fca5eb3c3521e3fa1b3beeb066acb15629deeb/airflow/serialization/serde.py#L273

### Are you willing to submit PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
