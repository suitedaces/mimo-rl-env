`logs` command for PipelineRun/Taskrun does not validate the `--limit` option to give an error if the limit is given <= 0

**tkn Version:**
Client version: 0.8.0

**Operating System:** 
Fedora 31

# Expected Behavior
$ tkn pr logs --limit 0
Error: limit was 0 but must be a positive number
$ tkn tr logs --limit 0
Error: limit was 0 but must be a positive number

# Actual Behavior
$ tkn pr logs --limit 0
Error: No pipelineruns found
$ tkn tr logs --limit 0
Error: No taskruns found
