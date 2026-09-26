### Custom Maven repositories declared with `url = uri(...)` are ignored

I have a `build.gradle` that declares a private Maven repository like this:

```groovy
repositories {
    mavenCentral()
    maven {
        url = uri('https://my.company.example.com/maven')
    }
}
```

Dependabot doesn't seem to pick up dependencies that live in this private repo — it behaves as if only `mavenCentral()` were declared. If I rewrite the same block as

```groovy
repositories {
    mavenCentral()
    maven {
        url = 'https://my.company.example.com/maven'
    }
}
```

then it works fine and Dependabot finds updates from the private repo.

The `uri(...)` form is the one Gradle's own docs use a lot, and `MavenArtifactRepository#setUrl` happily accepts anything that can be coerced to a URI, so people end up writing it in several equivalent ways, e.g.

```groovy
maven { url = uri('https://...') }                     // Project.uri helper
maven { url = URI.create('https://...') }              // java.net
maven { url = new java.net.URI('https://...') }
maven { url = 'https://...'.toURI() }                  // Groovy
maven { url = 'https://...' }                          // plain String
```

All of these are valid Gradle and resolve to the same repository, but only the last one is recognised today. It would be great if Dependabot recognised the wrapped forms too (at least the common `uri('…')` case) so we don't have to rewrite our build files just to make Dependabot happy.
