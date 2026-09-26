Message size limit should include message attributes
### Is there an existing issue for this?

- [X] I have searched the existing issues

### Current Behavior

With AWS, you can't send messages where the total size of message body + message attributes are greater than 262,144 bytes.

Currently, you are taking into account the message body only.

```python
>>> client = boto3.client('sqs', aws_access_key_id='fake', aws_secret_access_key='fake', endpoint_url='http://localstack:4566')
...
>>> client.send_message(QueueUrl='http://localstack:4566/000000000000/foo', MessageBody=('x' * 262_144), MessageAttributes={ 'k': { 'DataType': 'String', 'StringValue': 'v' } })
# the message is successfully delivered
{'MD5OfMessageBody': '1566aa66d825eb4354d3e9533b753995', 'MD5OfMessageAttributes': '731170ec8e13273a4e68fdcc2abaf9b4', 'MessageId': '6d12f05f-173f-45f2-a561-848070cd1390', 'ResponseMetadata': {'RequestId': 'DL5GNQG3WJ3IUOGTRD49RCG7DQAL333ZZNBP7RL8IEHAZVPMA367', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'text/xml', 'content-length': '493', 'connection': 'close', 'access-control-allow-origin': '*', 'access-control-allow-methods': 'HEAD,GET,PUT,POST,DELETE,OPTIONS,PATCH', 'access-control-allow-headers': 'authorization,cache-control,content-length,content-md5,content-type,etag,location,x-amz-acl,x-amz-content-sha256,x-amz-date,x-amz-request-id,x-amz-security-token,x-amz-tagging,x-amz-target,x-amz-user-agent,x-amz-version-id,x-amzn-requestid,x-localstack-target,amz-sdk-invocation-id,amz-sdk-request', 'access-control-expose-headers': 'etag,x-amz-version-id', 'date': 'Tue, 08 Nov 2022 20:56:15 GMT', 'server': 'hypercorn-h11'}, 'RetryAttempts': 0}}
```

### Expected Behavior

With AWS I obtain an error because the message attributes are taken into account when computing the message size:

```python
>>> client.send_message(QueueUrl=MY_QUEUE_URL, MessageBody=('x' * 262_144), MessageAttributes={ 'k': { 'DataType': 'String', 'StringValue': 'v' } })
# fail
botocore.exceptions.ClientError: An error occurred (InvalidParameterValue) when calling the SendMessage operation: One or more parameters are invalid. Reason: Message must be shorter than 262144 bytes.
```

In fact, if I subtract the byte size of the attribute values (`len('k')` + `len('String')` + `len('x')` = 8) from the message body I managed to send the message:

```python
>>> client.send_message(QueueUrl=MY_QUEUE_URL, MessageBody=('x' * 262_136), MessageAttributes={ 'k': { 'DataType': 'String', 'StringValue': 'v' } })
# the message is successfully delivered
```

### How are you starting LocalStack?

With a `docker run` command

### Steps To Reproduce

#### How are you starting localstack (e.g., `bin/localstack` command, arguments, or `docker-compose.yml`)

    docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack

#### Client commands (e.g., AWS SDK code snippet, or sequence of "awslocal" commands)

```python
import boto3

client = boto3.client('sqs', aws_access_key_id='fake', aws_secret_access_key='fake', endpoint_url='http://localstack:4566')
client.create_queue(QueueName='foo')
client.send_message(QueueUrl='http://localstack:4566/000000000000/foo', MessageBody=('x' * 262_144), MessageAttributes={ 'x': { 'DataType': 'String', 'StringValue': 'x' } })
```


### Environment

```markdown
- OS: Mac OS X Monterey
- LocalStack: 1.1.1
```


### Anything else?

If this bug is confirmed, I'd like to contribute by making a PR 😃
