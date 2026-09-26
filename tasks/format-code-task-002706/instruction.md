## Description

com.spotify.docker.client.exceptions.DockerRequestException: Request error: GET http://10.110.13.32:3375/containers/0d6e51015f514d09e6ed3d5/json: 200
	at com.spotify.docker.client.DefaultDockerClient.propagate(DefaultDockerClient.java:2103)
	at com.spotify.docker.client.DefaultDockerClient.request(DefaultDockerClient.java:2042)
	at com.spotify.docker.client.DefaultDockerClient.inspectContainer(DefaultDockerClient.java:901)
	at org.MainDocker.main(MainDocker.java:71)
Caused by: javax.ws.rs.client.ResponseProcessingException: com.fasterxml.jackson.databind.JsonMappingException: Instantiation of [simple type, class com.spotify.docker.client.messages.ContainerInfo$Node] value failed: Null id (through reference chain: com.spotify.docker.client.messages.ContainerInfo["Node"])
	....
Caused by: com.fasterxml.jackson.databind.JsonMappingException: Instantiation of [simple type, class com.spotify.docker.client.messages.ContainerInfo$Node] value failed: Null id (through reference chain: 
	... 17 more
**Caused by: java.lang.NullPointerException: Null id**
	at com.spotify.docker.client.messages.AutoValue_ContainerInfo_Node.<init>(AutoValue_ContainerInfo_Node.java:21)
	at com.fasterxml.jackson.databind.deser.std.StdValueInstantiator.createFromObjectWith(StdValueInstantiator.java:227)
	... 39 more

## How to reproduce
1.DockerClient docker = DefaultDockerClient.builder().uri(URI.create("http://10.110.13.32:3375")).build();
2.String id = "0d6e51015f514d09e6ed3d5";
3.ContainerInfo containerInfo = docker.inspectContainer(id);
"http://10.110.13.32:3375" is my swarm manager‘s address
## What do you expect
the container's information，then i can look up the networksetting.

## What happened instead
the error occured,error show me the id isnull

## Software:

Client:
 Version:      1.10.3
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   20f81dd
 Built:        Thu Mar 10 15:39:25 2016
 OS/Arch:      linux/amd64

Server:
 Version:      1.10.3
 API version:  1.22
 Go version:   go1.5.3
 Git commit:   20f81dd
 Built:        Thu Mar 10 15:39:25 2016
 OS/Arch:      linux/amd64
- `docker version`: [Add the output of `docker version` here, both client and server]
- Spotify's docker-client version: [Add docker-client version here]

## Full backtrace
Question：how should i use method “inspectContainer”? 
Thanks all！
```text
com.spotify.docker.client.exceptions.DockerRequestException: Request error: GET http://10.110.13.32:3375/containers/0d6e51015f514d09e6ed3d5/json: 200
	at com.spotify.docker.client.DefaultDockerClient.propagate(DefaultDockerClient.java:2103)
	at com.spotify.docker.client.DefaultDockerClient.request(DefaultDockerClient.java:2042)
	at com.spotify.docker.client.DefaultDockerClient.inspectContainer(DefaultDockerClient.java:901)
	at org.MainDocker.main(MainDocker.java:71)
Caused by: javax.ws.rs.client.ResponseProcessingException: com.fasterxml.jackson.databind.JsonMappingException: Instantiation of [simple type, class com.spotify.docker.client.messages.ContainerInfo$Node] value failed: Null id (through reference chain: com.spotify.docker.client.messages.ContainerInfo["Node"])
	at org.glassfish.jersey.client.JerseyInvocation.translate(JerseyInvocation.java:806)
	at org.glassfish.jersey.client.JerseyInvocation.access$700(JerseyInvocation.java:92)
	at org.glassfish.jersey.client.JerseyInvocation$5.completed(JerseyInvocation.java:773)
	at org.glassfish.jersey.client.ClientRuntime.processResponse(ClientRuntime.java:198)
	at org.glassfish.jersey.client.ClientRuntime.access$300(ClientRuntime.java:79)
	at org.glassfish.jersey.client.ClientRuntime$2.run(ClientRuntime.java:180)
	at org.glassfish.jersey.internal.Errors$1.call(Errors.java:271)
	at org.glassfish.jersey.internal.Errors$1.call(Errors.java:267)
	at org.glassfish.jersey.internal.Errors.process(Errors.java:315)
	at org.glassfish.jersey.internal.Errors.process(Errors.java:297)
	at org.glassfish.jersey.internal.Errors.process(Errors.java:267)
	at org.glassfish.jersey.process.internal.RequestScope.runInScope(RequestScope.java:340)
	at org.glassfish.jersey.client.ClientRuntime$3.run(ClientRuntime.java:210)
	at java.util.concurrent.Executors$RunnableAdapter.call(Unknown Source)
	at java.util.concurrent.FutureTask.run(Unknown Source)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
	at java.lang.Thread.run(Unknown Source)
Caused by: com.fasterxml.jackson.databind.JsonMappingException: Instantiation of [simple type, class com.spotify.docker.client.messages.ContainerInfo$Node] value failed: Null id (through reference chain: com.spotify.docker.client.messages.ContainerInfo["Node"])
	at com.fasterxml.jackson.databind.deser.std.StdValueInstantiator.wrapException(StdValueInstantiator.java:399)
	at com.fasterxml.jackson.databind.deser.std.StdValueInstantiator.createFromObjectWith(StdValueInstantiator.java:231)
	at com.fasterxml.jackson.databind.deser.impl.PropertyBasedCreator.build(PropertyBasedCreator.java:135)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeUsingPropertyBased(BeanDeserializer.java:440)
	at com.fasterxml.jackson.databind.deser.BeanDeserializerBase.deserializeFromObjectUsingNonDefault(BeanDeserializerBase.java:1100)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserializeFromObject(BeanDeserializer.java:294)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserialize(BeanDeserializer.java:131)
	at com.fasterxml.jackson.databind.deser.SettableBeanProperty.deserialize(SettableBeanProperty.java:520)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeWithErrorWrapping(BeanDeserializer.java:461)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserializeUsingPropertyBased(BeanDeserializer.java:377)
	at com.fasterxml.jackson.databind.deser.BeanDeserializerBase.deserializeFromObjectUsingNonDefault(BeanDeserializerBase.java:1100)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserializeFromObject(BeanDeserializer.java:294)
	at com.fasterxml.jackson.databind.deser.BeanDeserializer.deserialize(BeanDeserializer.java:131)
	at com.fasterxml.jackson.databind.ObjectReader._bind(ObjectReader.java:1470)
	at com.fasterxml.jackson.databind.ObjectReader.readValue(ObjectReader.java:912)
	at com.fasterxml.jackson.jaxrs.base.ProviderBase.readFrom(ProviderBase.java:811)
	at org.glassfish.jersey.message.internal.ReaderInterceptorExecutor$TerminalReaderInterceptor.invokeReadFrom(ReaderInterceptorExecutor.java:256)
	at org.glassfish.jersey.message.internal.ReaderInterceptorExecutor$TerminalReaderInterceptor.aroundReadFrom(ReaderInterceptorExecutor.java:235)
	at org.glassfish.jersey.message.internal.ReaderInterceptorExecutor.proceed(ReaderInterceptorExecutor.java:155)
	at org.glassfish.jersey.message.internal.MessageBodyFactory.readFrom(MessageBodyFactory.java:1085)
	at org.glassfish.jersey.message.internal.InboundMessageContext.readEntity(InboundMessageContext.java:874)
	at org.glassfish.jersey.message.internal.InboundMessageContext.readEntity(InboundMessageContext.java:808)
	at org.glassfish.jersey.client.ClientResponse.readEntity(ClientResponse.java:326)
	at org.glassfish.jersey.client.JerseyInvocation.translate(JerseyInvocation.java:803)
	... 17 more
Caused by: java.lang.NullPointerException: Null id
	at com.spotify.docker.client.messages.AutoValue_ContainerInfo_Node.<init>(AutoValue_ContainerInfo_Node.java:21)
	at com.spotify.docker.client.messages.ContainerInfo$Node.create(ContainerInfo.java:209)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(Unknown Source)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)
	at java.lang.reflect.Method.invoke(Unknown Source)
	at com.fasterxml.jackson.databind.introspect.AnnotatedMethod.call(AnnotatedMethod.java:120)
	at com.fasterxml.jackson.databind.deser.std.StdValueInstantiator.createFromObjectWith(StdValueInstantiator.java:227)
	... 39 more
```
