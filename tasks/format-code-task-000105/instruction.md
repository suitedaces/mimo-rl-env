Copying symlink from previous stage fails instead of overwriting
**Actual behavior**
`COPY --from=0 X Y` where X is a symlink from stage 0 and Y is an pre-existing symlink in the current stage fails with "file exists".

**Expected behavior**
`COPY --from=0 X Y` where X is a symlink from stage 0 and Y is a pre-existing symlink in the current stage should overwrite Y with X as it would if neither were symlinks.

**To Reproduce**

```bash
docker run --rm -v $PWD:/workspace:ro gcr.io/kaniko-project/executor:v0.6.0 --no-push
```
with the following Dockerfile:
```dockerfile
FROM python:slim

FROM python:slim
COPY --from=0 /usr/local/lib/libpython3.7m.so /usr/local/lib/libpython3.7m.so
```

Although this is a bit contrived, we had a Dockerfile which was building into /usr/local/lib and then copying that into the final stage which seems like a legitimate use-case.
