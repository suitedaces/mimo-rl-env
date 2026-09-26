SSLTransport error: unexpected keyword argument 'ca_certs'
Using amqp version 5.0.1, I discovered an SSLTransport error. When I use amqp version 5.0.0b1, SSL works just fine.

Here's the error I get when using amqp==5.0.1:

`/usr/local/lib/python3.8/dist-packages/kombu/connection.py:283: in channel
    chan = self.transport.create_channel(self.connection)
/usr/local/lib/python3.8/dist-packages/kombu/connection.py:858: in connection
    return self._ensure_connection(
/usr/local/lib/python3.8/dist-packages/kombu/connection.py:435: in _ensure_connection
    return retry_over_time(
/usr/local/lib/python3.8/dist-packages/kombu/utils/functional.py:325: in retry_over_time
    return fun(*args, **kwargs)
/usr/local/lib/python3.8/dist-packages/kombu/connection.py:866: in _connection_factory
    self._connection = self._establish_connection()
/usr/local/lib/python3.8/dist-packages/kombu/connection.py:801: in _establish_connection
    conn = self.transport.establish_connection()
/usr/local/lib/python3.8/dist-packages/kombu/transport/pyamqp.py:128: in establish_connection
    conn.connect()
/usr/local/lib/python3.8/dist-packages/amqp/connection.py:314: in connect
    self.transport.connect()
/usr/local/lib/python3.8/dist-packages/amqp/transport.py:77: in connect
    self._init_socket(
/usr/local/lib/python3.8/dist-packages/amqp/transport.py:188: in _init_socket
    self._setup_transport()
/usr/local/lib/python3.8/dist-packages/amqp/transport.py:323: in _setup_transport
    self.sock = self._wrap_socket(self.sock, **self.sslopts)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <amqp.transport.SSLTransport object at 0x7f8a0083a370>
sock = <socket.socket fd=11, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=6, laddr=('127.0.0.1', 41008), raddr=('127.0.0.1', 5671)>
context = None
sslopts = {'ca_certs': '/home/cameron/Defense/tls-gen/basic/result/ca_certificate.pem', 'cert_reqs': <VerifyMode.CERT_REQUIRED: ...e/tls-gen/basic/result/client_certificate.pem', 'keyfile': '/home/cameron/Defense/tls-gen/basic/result/client_key.pem'}

    def _wrap_socket(self, sock, context=None, **sslopts):
        if context:
            return self._wrap_context(sock, sslopts, **context)
>       return self._wrap_socket_sni(sock, **sslopts)
E       TypeError: _wrap_socket_sni() got an unexpected keyword argument 'ca_certs'

/usr/local/lib/python3.8/dist-packages/amqp/transport.py:330: TypeError
----------------------------------------------------------- Captured stdout call -----------------------------------------------------------
2020-10-28 16:46:54:	INFO:	Consumer successfully connected to kombu server at localhost:5671
2020-10-28 16:46:54:	ERROR:	Failed to initialize rabbit consumer connection:
Traceback (most recent call last):
TypeError: _wrap_socket_sni() got an unexpected keyword argument 'ca_certs'`

Looking at `py-amqp/amqp/transport.py`, the parameters for the method `_wrap_socket_sni` for amqp==5.0.1, it doesn't include `ca_certs`. On amqp==5.0.0b1, the method _wrap_socket_sni` does include `ca_certs` as a parameter. Is this a bug or was this left out by accident?

Here are the links to amqp version 5.0.1 and 5.0.0b1 of `py-amqp/amqp/transport.py` with the line numbers highlighting the method:
amqp==5.0.1: https://github.com/celery/py-amqp/blob/93e4f3a2990f2ed1a6da861c99c7f0a3b0d32160/amqp/transport.py#L337
amqp==5.0.0b1: https://github.com/celery/py-amqp/blob/c5fe7daaf379cfbcccbe81fcd1ea12807274f8fb/amqp/transport.py#L339
