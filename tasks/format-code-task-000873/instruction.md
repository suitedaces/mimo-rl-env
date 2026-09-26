Errors are not written to `STDERR`
A missing dependency detected by [quaertym/ember-cli-dependency-checker](https://github.com/quaertym/ember-cli-dependency-checker/blob/master/lib/reporter.js#L65) raises an Error.

EmberCLI logs the error to `STDOUT`, but not the `STDERR`:

``` bash
2.2.3 in frontend/ on master 
› rm -rf node_modules/ember-data

2.2.3 in frontend/ on master 
› ember build 2> tmp/stderr.txt 

Missing npm packages: 
Package: ember-data
  * Specified: 2.1.0
  * Installed: (not installed)

Run `npm install` to install missing dependencies.


2.2.3 in frontend/ on master 
› cat tmp/stderr.txt 

2.2.3 in frontend/ on master 
› 
```
