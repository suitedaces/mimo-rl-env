[DEVEL] httpGet is passing URL.path incorrectly
**Description**
httpGet is passing URL.path incorrectly. 
For example,
when to request a task for httpGet with API URL, such as "https://api.nasa.gov/insight_weather/?api_key=eTitgeQIgcVYEqKbEfToPyG1r1GVVbaV4SKC7vwe&feedtype=json&ver=1.0", the chainlink node pass url with "https://api.nasa.gov/insight_weather?api_key=eTitgeQIgcVYEqKbEfToPyG1r1GVVbaV4SKC7vwe&feedtype=json&ver=1.0" instead. Where the slash after insight_weather are missing.

**Your Environment**
Go, Docker

**Basic Information**
in http.go line 124, path.Join() may remote the tailing slashes. 

**Steps to Reproduce**
send above API  URL with a httpGet task will see the return is not in JSON with data as expected.

**Additional Information**
check [http.go](https://github.com/smartcontractkit/chainlink/blob/7391acf38718659fb850f5b8c837f035a160b1f2/core/adapters/http.go) line 124, compared it with this testing in https://play.golang.org/p/tV87gXCuu8e
You can see path.Join() in the appendExtendedPath() function actually remove the tailing slashes. That cause the problem.
