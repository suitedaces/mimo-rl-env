Runaway program detector errors have no location information
Example:

```
$ bin/juttle -e 'read file -file "xxx" -from :beginning: -to :end: | tail 1'
Error: Not starting program as it would run forever with no output. Add a -to option to read?
```
