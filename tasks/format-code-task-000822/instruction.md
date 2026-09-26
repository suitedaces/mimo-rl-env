docker-machine scp does not use the SSH port specified in ~/.docker/machine/machines/<machine>/config.json
I have the following in my machine config:

```
{
    "ConfigVersion": 3,
    "Driver": {
        "IPAddress": ...,
        "MachineName": ...,
        "SSHUser": "root",
        "SSHPort": 2222,
        "SSHKeyPath": "/Users/cyli/.docker/machine/machines/<machine>/id_rsa",
        "StorePath": "/Users/cyli/.docker/machine",
        "SwarmMaster": false,
        "SwarmHost": "tcp://0.0.0.0:3376",
        "SwarmDiscovery": "",
        "AccessToken": ...,
        "DropletID": ...,
        "DropletName": "",
        "Image": "ubuntu-15-10-x64",
        "Region": "nyc3",
        "SSHKeyID": 2013668,
        "SSHKeyFingerprint": "",
        "Size": "4GB",
        "IPv6": false,
        "Backups": false,
        "PrivateNetworking": false,
        "UserDataFile": ""
    },
    ...
```

`docker-machine ssh` successfully connects to my Droplet.

When I run `docker-machine scp myfile.txt <machine-name>:myfile.txt` I get the following:

```
Docker Machine Version:  0.7.0, build a650a40
Found binary path at /usr/local/bin/docker-machine
Launching plugin server for driver digitalocean
Plugin server listening at address 127.0.0.1:56808
() Calling .GetVersion
Using API Version  1
() Calling .SetConfigRaw
() Calling .GetMachineName
(<machine-name>) Calling .GetSSHKeyPath
(<machine-name>) Calling .GetSSHKeyPath
(<machine-name>) Calling .GetIP
(<machine-name>) Calling .GetSSHUsername
{/usr/bin/scp [/usr/bin/scp -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet -3 -i /Users/cyli/.docker/machine/machines/<machine-name>/id_rsa myfile.txt root@104.131.33.10:myfile.txt] []  <nil> <nil> <nil> [] <nil> <nil> <nil> <nil> false [] [] [] [] <nil>}
lost connection
exit status 1
```

The port value for scp can be specified with a `-P` option on mac os and the flavors of ubuntu I've used.  Not sure if this is generalizable to all platforms supported by docker-machine.
