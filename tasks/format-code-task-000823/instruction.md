docker-compose fails if using secrets file
## Environment

```
$ docker --version
Docker version 1.13.1, build 092cba3
$ docker-compose --version
docker-compose version 1.11.1, build 7c5d5e4
```

## Steps to reproduce
```
$ ls
docker-compose.yml	my_file_secret.txt
$ cat my_file_secret.txt 
This is a file secret.
$ cat docker-compose.yml 
version: '3.1'

services:
  a: 
    image: tutum/hello-world
  b:
    image: tutum/hello-world
    secrets:
      - my_file_secret

secrets:
  my_file_secret:
    file: my_file_secret.txt
```

```
$ docker-compose up
Traceback (most recent call last):
  File "docker-compose", line 3, in <module>
  File "compose/cli/main.py", line 88, in main
  File "compose/cli/main.py", line 137, in perform_command
  File "compose/cli/command.py", line 36, in project_from_options
  File "compose/cli/command.py", line 115, in get_project
  File "compose/project.py", line 110, in from_config
  File "compose/project.py", line 566, in get_secrets
AttributeError: 'str' object has no attribute 'source'
Failed to execute script docker-compose
```
