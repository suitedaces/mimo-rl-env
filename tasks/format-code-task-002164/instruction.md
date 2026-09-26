**Generated Dockerfile doesn't take advantage of Docker layer caching on rebuilds**

When I make a small change to my operator's Go code and rebuild the image, I notice the `docker build` step is doing more work than it should. I'm using the Dockerfile that `operator-sdk new ...` scaffolds out into `tmp/build/Dockerfile`, which looks like:

```dockerfile
FROM alpine:3.6

ADD tmp/_output/bin/<project> /usr/local/bin/<project>

RUN adduser -D <project>
USER <project>
```

My normal dev loop is: edit a Go file → rebuild the binary → `docker build` → push → `kubectl apply`. Because the binary that gets ADDed is essentially different on every build (new Go output), Docker invalidates that layer on every iteration. Given how layer caching works, that means everything in the Dockerfile after the `ADD` also has to be redone — including the `adduser` step, which has nothing to do with the binary content and never actually changes between builds.

In a tight edit→build→deploy cycle I end up paying for `adduser` (and any layers after it) every single round trip, when really the only thing that differs between two consecutive builds is the binary itself.

It would be nice if the scaffolded Dockerfile were arranged so that during normal iteration only the layer that carries the new binary needs to be rebuilt, and the layers that aren't a function of the binary stay cached.
