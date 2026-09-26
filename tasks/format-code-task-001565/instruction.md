sqlserver input exclude_query config option may be confusing
## Feature Request
Excluding what you do not want instead of including what you do want to monitor may get confusing, specially when you just need a few measurements.

### Proposal:
Deprecate exclude_query configuration option and include a new one to indicate which query metrics one wants to run.

### Current behavior:
It is necessary to explicitly state which queries one does not want to be executed when the sqlserver plugin is enabled.

### Desired behavior:
None query is executed unless explicitly stated to do so in the config file.

### Use case: <!-- [Why is this important (helps with prioritizing requests)] -->
Supose that I only want to keep track of database IO every 30s and wait stats every 60s. The config file would look something like this:

> [[inputs.sqlserver]]
  interval = "30s"
  servers = [
	"Server=server;Port=port;User Id=telegraf;Password=password;app name=telegraf;log=1;",
  ]
>  \#
>  \## Optional parameter, setting this to two will use a new version
>  \## of the collection queries that break compatibility with the original
>  \## dashboards. 
>  query_version = 2
>  \## If you are using AzureDB, setting this to True will gather resource utilization metrics
>  \# azuredb = False
>  \## If you would like to exclude some of the metrics queries, list them here
>  \## Possible choices:
>  \## - PerformanceCounters
>  \## - WaitStatsCategorized
>  \## - DatabaseIO
>  \## - DatabaseProperties
>  \## - CPUHistory
>  \## - DatabaseSize
>  \## - DatabaseStats
>  \## - MemoryClerk
>  \## - VolumeSpace
>  \## - Schedulers
>  \## - AzureDBResourceStats
>  \## - AzureDBResourceGovernance
>  \## - SqlRequests
>  \## - ServerProperties
>  **exclude_query = [ 'PerformanceCounters', 'WaitStatsCategorized', 'DatabaseProperties', 'CPUHistory', 'DatabaseSize', 'DatabaseStats', 'MemoryClerk', 'VolumeSpace', 'VolumeSpace', 'Schedulers', 'AzureDBResourceStats', 'AzureDBResourceGovernance', 'SqlRequests', 'ServerProperties' ]**
>  [[inputs.sqlserver]]
  interval = "60s"
  servers = [
	"Server=server;Port=port;User Id=telegraf;Password=password;app name=telegraf;log=1;",
  ]
>  \#
>  \## Optional parameter, setting this to two will use a new version
>  \## of the collection queries that break compatibility with the original
>  \## dashboards. 
>  query_version = 2
>  \## If you are using AzureDB, setting this to True will gather resource utilization metrics
>  \# azuredb = False
>  \## If you would like to exclude some of the metrics queries, list them here
>  \## Possible choices:
>  \## - PerformanceCounters
>  \## - WaitStatsCategorized
>  \## - DatabaseIO
>  \## - DatabaseProperties
>  \## - CPUHistory
>  \## - DatabaseSize
>  \## - DatabaseStats
>  \## - MemoryClerk
>  \## - VolumeSpace
>  \## - Schedulers
>  \## - AzureDBResourceStats
>  \## - AzureDBResourceGovernance
>  \## - SqlRequests
>  \## - ServerProperties
>  **exclude_query = [ 'PerformanceCounters', 'DatabaseIO', 'DatabaseProperties', 'CPUHistory', 'DatabaseSize', 'DatabaseStats', 'MemoryClerk', 'VolumeSpace', 'VolumeSpace', 'Schedulers', 'AzureDBResourceStats', 'AzureDBResourceGovernance', 'SqlRequests', 'ServerProperties' ]**

It is not clear what I wanted to monitor at all. Instead, it would be a lot clearer if the config file read like this: 

>  [[inputs.sqlserver]]
  interval = "30s"
  servers = [
	"Server=server;Port=port;User Id=telegraf;Password=password;app name=telegraf;log=1;",
  ]
>  \#
>  \## Optional parameter, setting this to two will use a new version
>  \## of the collection queries that break compatibility with the original
>  \## dashboards. 
>  query_version = 2
>  \## If you are using AzureDB, setting this to True will gather resource utilization metrics
>  \# azuredb = False
>  \## Metrics queries
>  \## Possible choices:
>  \## - PerformanceCounters
>  \## - WaitStatsCategorized
>  \## - DatabaseIO
>  \## - DatabaseProperties
>  \## - CPUHistory
>  \## - DatabaseSize
>  \## - DatabaseStats
>  \## - MemoryClerk
>  \## - VolumeSpace
>  \## - Schedulers
>  \## - AzureDBResourceStats
>  \## - AzureDBResourceGovernance
>  \## - SqlRequests
>  \## - ServerProperties
>  **metrics_queries = [ 'DatabaseIO' ]**
>  [[inputs.sqlserver]]
  interval = "60s"
  servers = [
	"Server=server;Port=port;User Id=telegraf;Password=password;app name=telegraf;log=1;",
  ]
>  \#
>  \## Optional parameter, setting this to two will use a new version
>  \## of the collection queries that break compatibility with the original
>  \## dashboards. 
>  query_version = 2
>  \## If you are using AzureDB, setting this to True will gather resource utilization metrics
>  \# azuredb = False
>  \## Metrics queries
>  \## Possible choices:
>  \## - PerformanceCounters
>  \## - WaitStatsCategorized
>  \## - DatabaseIO
>  \## - DatabaseProperties
>  \## - CPUHistory
>  \## - DatabaseSize
>  \## - DatabaseStats
>  \## - MemoryClerk
>  \## - VolumeSpace
>  \## - Schedulers
>  \## - AzureDBResourceStats
>  \## - AzureDBResourceGovernance
>  \## - SqlRequests
>  \## - ServerProperties
>  **metrics_queries = [ 'WaitStatsCategorized' ]**
