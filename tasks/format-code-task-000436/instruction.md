## Support graphql-java 14

`federation-jvm` is currently pinned to `graphql-java` 13.0 (see `graphql-java.version` in the parent `pom.xml`). graphql-java 14 has been out for a while now and we'd like to be able to use it together with this library.

When I tried to override the `graphql-java` version to 14 in my own project (which depends on `graphql-java-support`), the build no longer compiles — there are a number of source-incompatible API changes between graphql-java 13 and 14 that this module hits directly. So just bumping the dependency in a downstream consumer doesn't work, the library itself needs to be updated.

Could the `graphql-java` dependency be bumped to 14 and the code adapted accordingly?

I understand this would be a backwards-incompatible change for consumers that are still on 13, but at this point I think it's worth it — staying on 13 is becoming a real problem for projects that want to take advantage of fixes/features in newer graphql-java releases.

For reference, my use case is a federated subgraph built with `Federation.transform(...)`, exposed via `_service { sdl }` to an Apollo gateway, so anything around schema generation, the runtime wiring, and the SDL printing path needs to keep working end-to-end after the upgrade (the SDL has to be something the gateway will accept for composition).
