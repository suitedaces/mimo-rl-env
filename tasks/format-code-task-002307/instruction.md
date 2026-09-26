Failure to get the container id
With #1888 in place, there's a regression when running inside a container. There's an assumption in https://github.com/pre-commit/pre-commit/blob/master/pre_commit/languages/docker.py#L32 that the hostname is the container ID which is not always the case (it's easy enough to set a different hostname with `docker run --hostname foo`). It causes the `docker inspect` command that follows to fail. A more reliable way to get the container id is from `/proc/1/cpuset` or from the first line in `/proc/1/cgroup` which is already checked in `_is_in_docker`.

Thanks @asottile and @okainov for your work on #1387 and pre-commit in general.
