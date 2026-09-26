Allow better filtering of event logs (audit log)
### What do you see as an issue?

The REST API get event logs endpoint only allows filtering logs by a single event type. This only includes that one event type and all others are discarded. One cannot filter out even a single event type.

### Solving the problem

In order to use this fully, I think we need to be able to pass multiple event names and also specify if we are including or excluding them.

In the webserver we use `audit_view_excluded_events` and `audit_view_included_events`. We should have something similar for the rest API for a user to specify what they want to include and exclude.

### Anything else

_No response_

### Are you willing to submit PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
