1. Please describe the issue you observed:
    1. start local RocketMQ cluster 
    2. use example/consumer/simple/main.go start a consumer.
    3. use ./mqadmin resetOffset tool to reset offset.
    4. consumer process exit with.
   
          INFO[0005] receive reset consumer offset request...      broker="127.0.0.1:30931" consumerGroup=groupB timestamp=631123200000 topic=topicB
panic: runtime error: index out of range [1] with length 1
goroutine 113 [running]:
github.com/apache/rocketmq-client-go/v2/internal.(*ResetOffsetBody).Decode(0xc000461d20, {0xc00040c100, 0xfd, 0xfd})
        /Users/bytedance/github/rocketmq-client-go/internal/model.go:309 +0xa45
github.com/apache/rocketmq-client-go/v2/internal.GetOrNewRocketMQClient.func5(0xc000416a80, {0x14ed5c8, 0xc0003260c0})
        /Users/bytedance/github/rocketmq-client-go/internal/client.go:303 +0x3f8
github.com/apache/rocketmq-client-go/v2/internal/remote.(*remotingClient).processCMD.func2()
        /Users/bytedance/github/rocketmq-client-go/internal/remote/remote_client.go:207 +0x94
github.com/apache/rocketmq-client-go/v2/primitive.WithRecover(0xc000421ef0)
        /Users/bytedance/github/rocketmq-client-go/primitive/base.go:100 +0x47
created by github.com/apache/rocketmq-client-go/v2/internal/remote.(*remotingClient).processCMD
        /Users/bytedance/github/rocketmq-client-go/internal/remote/remote_client.go:206 +0x378
Exiting.
    ```

2. Please tell us about your environment:
    mac local 
    master client-go code.
    rocketmq broker with fastjson-1.2.76.jar

3. Other information (e.g. detailed explanation, logs, related issues, suggestions on how to fix, etc):
the test code in decode ResetOffsetBody json format is different from mine

mine from rocketmq broker response rpc
```json
{"offsetTable":{{"brokerName":"RaftNode00","queueId":0,"topic":"topicB"}:0,{"brokerName":"RaftNode00","queueId":1,"topic":"topicB"}:0,{"brokerName":"RaftNode00","queueId":2,"topic":"topicB"}:0,{"brokerName":"RaftNode00","queueId":3,"topic":"topicB"}:0}}
```

any different from fastjson config ?
