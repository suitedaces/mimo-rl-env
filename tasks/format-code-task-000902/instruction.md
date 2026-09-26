"ethclient.Client" doesn't support setting http header.
While i use infura jsonapi with "ethclient.Client", for security considerations, i gonna set "User-Agent", "Origin" by HTTP Headers.
But i can't find a way to do so.
Do i miss something ?

#### System information

Geth version: `v1.9.5`
OS & Version: ubuntu 18.04.01 

#### Expected behaviour


#### Actual behaviour


#### Steps to reproduce the behaviour


#### Backtrace

````
[backtrace]
````

It would be nice if the underlying rpc client exposed something like `SetHeader(key, value)` for this.
