Trying to launch thumbor with a unix socket ends with "No such device or address"
Hi,

I'm trying to make thumbor listen to an Unix socket instead of port (and to automate this _via_ systemd but that's another story).

```shell
$ ls -al /run/thumbor/
total 0
drwxr-xr-x  2 root    root      60 Feb 23 15:51 .
drwxr-xr-x 27 root    root     880 Feb 23 15:18 ..
srw-rw-rw-  1 thumbor www-data   0 Feb 23 15:18 thumbor.sock

$ sudo -u thumbor /usr/local/bin/thumbor --fd /run/thumbor/thumbor.sock
Traceback (most recent call last):
  File "/usr/local/bin/thumbor", line 10, in <module>
    sys.exit(main())
  File "/usr/local/lib/python2.7/dist-packages/thumbor/server.py", line 147, in main
    server = run_server(application, context)
  File "/usr/local/lib/python2.7/dist-packages/thumbor/server.py", line 118, in run_server
    with open(context.server.fd, 'r') as sock:
IOError: [Errno 6] No such device or address: '/run/thumbor/thumbor.sock'
```

A simple `/usr/local/bin/thumbor --fd /run/thumbor/thumbor.sock` ends the same, so I don't think it's a permission problem.

### Expected behaviour

The `--fd` option is announced to accept either a file descriptor or a path but it seems paths are not handled correctly.

I tried to use a simple file instead of a socket and ended with a "Bad file descriptor" error so I suppose the file has to be a socket. The `/run/thumbor/thumbor.sock` in my example has been created by systemd so I bet it's a valid Unix socket that should be supported out of the box.

I can see [a similar problems have been reported in the past](https://github.com/thumbor/thumbor/issues/929) but I can't use the same workaround as I'm not using Supervisor and the file descriptor for my socket will neither be 0 nor be predictible.

Am I missing something?
