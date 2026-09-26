when influxdb server shutdown, client still send metric,  the background goroutine "w.writeProc()" will crash at rand.Intn() after try 52 times
### Specifications

* Client Version: v2.12.0
* InfluxDB Version: v2.5.0
* Platform:  Ubuntu 20.04.5 LTS


### Steps to reproduce

1. influxdb server is not start, that is shutdown
2.  write points using lib to send metrics to server which in fact is not started
```
        dbClient := influxdb2.NewClient(serverUrl, token)
	dbClient.Options().WriteOptions().SetPrecision(time.Millisecond)
	defer dbClient.Close()
        dbWriteAPI := dbClient.WriteAPI("myorg", "mybucket")
        for {
		req, ok := <-gRecvChannel
		var metricName string
		if !ok {
			break
		}
                //........code about set metricName and tags
                p := influxdb2.NewPoint(metricName, tags,
				map[string]interface{}{"value": value},
				time.UnixMilli(timestamp))
		dbWriteAPI.WritePoint(p)
      }
```
3. at first, only print log like "dial tcp 127.0.0.1:8086: connect: connection refused, batch kept for retrying", but finally crash


### Expected behavior

at normal case, will print the follow log

2022/11/11 10:34:39 influxdb2client E! Write error: Post "http://127.0.0.1:8086/api/v2/write?bucket=mybucket&org=myorg&precision=ms": dial tcp 127.0.0.1:8086: connect: connection refused, batch kept for retrying
2022/11/11 10:34:39 influxdb2client E! Error flushing batch from retry queue: %!w(*url.Error=&{Post http://127.0.0.1:8086/api/v2/write?bucket=mybucket&org=myorg&precision=ms 0xc00022ceb0})
......
2022/11/11 10:47:09 influxdb2client E! Error flushing batch from retry queue: %!w(*url.Error=&{Post http://127.0.0.1:8086/api/v2/write?bucket=mybucket&org=myorg&precision=ms 0xc00022c1e0})
2022/11/11 10:47:24 influxdb2client E! Write error: Post "http://127.0.0.1:8086/api/v2/write?bucket=mybucket&org=myorg&precision=ms": dial tcp 127.0.0.1:8086: connect: connection refused, batch kept for retrying

### Actual behavior

but after about 13 minutes, panic crash, the call stack is as follow
```
runtime.fatalpanic (/usr/local/go/src/runtime/panic.go:1143)
runtime.gopanic (/usr/local/go/src/runtime/panic.go:987)
math/rand.(*Rand).Intn (/usr/local/go/src/math/rand/rand.go:168)
math/rand.Intn (/usr/local/go/src/math/rand/rand.go:337)
github.com/influxdata/influxdb-client-go/v2/internal/write.(*Service).computeRetryDelay (pkg/mod/github.com/influxdata/influxdb-client-go/v2@v2.12.0/internal/write/service.go:258)
github.com/influxdata/influxdb-client-go/v2/internal/write.(*Service).HandleWrite (pkg/mod/github.com/influxdata/influxdb-client-go/v2@v2.12.0/internal/write/service.go:175)
github.com/influxdata/influxdb-client-go/v2/api.(*WriteAPIImpl).writeProc (pkg/mod/github.com/influxdata/influxdb-client-go/v2@v2.12.0/api/write.go:192)
github.com/influxdata/influxdb-client-go/v2/api.NewWriteAPI.func2 (pkg/mod/github.com/influxdata/influxdb-client-go/v2@v2.12.0/api/write.go:92)
runtime.goexit (/usr/local/go/src/runtime/asm_amd64.s:1594)
```

### Additional info

i modify the code of  function "computeRetryDelay" at Go_Path/pkg/mod/github.com/influxdata/influxdb-client-go/v2@v2.12.0/internal/write/service.go,  print some logs
```
func (w *Service) computeRetryDelay(attempts uint) uint {
	minDelay := int(w.writeOptions.RetryInterval() * pow(w.writeOptions.ExponentialBase(), attempts))
	maxDelay := int(w.writeOptions.RetryInterval() * pow(w.writeOptions.ExponentialBase(), attempts+1))
	gTryCnt++ //added by me
	fmt.Printf("tryCnt=%5d maxDelay=%d minDelay=%d\n", gTryCnt, maxDelay, minDelay) //added by me
	retryDelay := uint(rand.Intn(maxDelay-minDelay) + minDelay)
	if retryDelay > w.writeOptions.MaxRetryInterval() {
		retryDelay = w.writeOptions.MaxRetryInterval()
	}
	return retryDelay
}
```
tryCnt=  1 maxDelay=10000 minDelay=5000
tryCnt=  2 maxDelay=20000 minDelay=10000
tryCnt=  3 maxDelay=40000 minDelay=20000
tryCnt=  4 maxDelay=80000 minDelay=40000
tryCnt=  5 maxDelay=160000 minDelay=80000
tryCnt=  6 maxDelay=320000 minDelay=160000
tryCnt=  7 maxDelay=640000 minDelay=320000
tryCnt=  8 maxDelay=1280000 minDelay=640000
tryCnt=  9 maxDelay=2560000 minDelay=1280000
tryCnt= 10 maxDelay=5120000 minDelay=2560000
tryCnt= 11 maxDelay=10240000 minDelay=5120000
tryCnt= 12 maxDelay=20480000 minDelay=10240000
tryCnt= 13 maxDelay=40960000 minDelay=20480000
tryCnt= 14 maxDelay=81920000 minDelay=40960000
tryCnt= 15 maxDelay=163840000 minDelay=81920000
tryCnt= 16 maxDelay=327680000 minDelay=163840000
tryCnt= 17 maxDelay=655360000 minDelay=327680000
tryCnt= 18 maxDelay=1310720000 minDelay=655360000
tryCnt= 19 maxDelay=2621440000 minDelay=1310720000
tryCnt= 20 maxDelay=5242880000 minDelay=2621440000
tryCnt= 21 maxDelay=10485760000 minDelay=5242880000
tryCnt= 22 maxDelay=20971520000 minDelay=10485760000
tryCnt= 23 maxDelay=41943040000 minDelay=20971520000
tryCnt= 24 maxDelay=83886080000 minDelay=41943040000
tryCnt= 25 maxDelay=167772160000 minDelay=83886080000
tryCnt= 26 maxDelay=335544320000 minDelay=167772160000
tryCnt= 27 maxDelay=671088640000 minDelay=335544320000
tryCnt= 28 maxDelay=1342177280000 minDelay=671088640000
tryCnt= 29 maxDelay=2684354560000 minDelay=1342177280000
tryCnt= 30 maxDelay=5368709120000 minDelay=2684354560000
tryCnt= 31 maxDelay=10737418240000 minDelay=5368709120000
tryCnt= 32 maxDelay=21474836480000 minDelay=10737418240000
tryCnt= 33 maxDelay=42949672960000 minDelay=21474836480000
tryCnt= 34 maxDelay=85899345920000 minDelay=42949672960000
tryCnt= 35 maxDelay=171798691840000 minDelay=85899345920000
tryCnt= 36 maxDelay=343597383680000 minDelay=171798691840000
tryCnt= 37 maxDelay=687194767360000 minDelay=343597383680000
tryCnt= 38 maxDelay=1374389534720000 minDelay=687194767360000
tryCnt= 39 maxDelay=2748779069440000 minDelay=1374389534720000
tryCnt= 40 maxDelay=5497558138880000 minDelay=2748779069440000
tryCnt= 41 maxDelay=10995116277760000 minDelay=5497558138880000
tryCnt= 42 maxDelay=21990232555520000 minDelay=10995116277760000
tryCnt= 43 maxDelay=43980465111040000 minDelay=21990232555520000
tryCnt= 44 maxDelay=87960930222080000 minDelay=43980465111040000
tryCnt= 45 maxDelay=175921860444160000 minDelay=87960930222080000
tryCnt= 46 maxDelay=351843720888320000 minDelay=175921860444160000
tryCnt= 47 maxDelay=703687441776640000 minDelay=351843720888320000
tryCnt= 48 maxDelay=1407374883553280000 minDelay=703687441776640000
tryCnt= 49 maxDelay=2814749767106560000 minDelay=1407374883553280000
tryCnt= 50 maxDelay=5629499534213120000 minDelay=2814749767106560000
tryCnt= 51 maxDelay=-7187745005283311616 minDelay=5629499534213120000
tryCnt= 52 maxDelay=4071254063142928384 minDelay=-7187745005283311616

so when maxDelay=4071254063142928384 minDelay=-7187745005283311616
maxDelay-minDelay = -7187745005283311616 < 0, so will panic at  "rand.Intn()" 

because  https://pkg.go.dev/math/rand#Intn  said: 

Intn returns, as an int, a non-negative pseudo-random number in the half-open interval [0,n) from the default Source.
 It panics if n <= 0.
