Cannot set custom jest commandline options
Currently there's no API/configuration to add extra options to the jest commandline invocation for the `test` task.

Being able to pass extra flags is useful to access certain behaviors of jest.

A practical use case is to enable json output to a file ( `--json --outputFile=jest-report.json` ) which is used by some external tools to render coverage reports
