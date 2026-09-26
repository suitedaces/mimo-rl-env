## Chaining multiple `@JoinFetch` annotations that share the same alias breaks the third fetch

I'm trying to use `@JoinFetch` to eagerly fetch a couple of independent associations off the same parent entity, while reusing an alias so I don't repeat the parent join. My setup on the controller method looks roughly like this:

```java
@JoinFetch(paths = "orders", alias = "o")
@JoinFetch(paths = "o.tags")
@JoinFetch(paths = "o.note")
```

`tags` and `note` are two separate associations on the `Orders` entity. My intent is "join-fetch orders once, then also fetch its tags and its note off that same join".

When the request hits, I get:

```
org.springframework.dao.InvalidDataAccessApiUsageException:
Unable to locate Attribute  with the the given name [note] on this ManagedType
[net.kaczmarzyk.spring.data.jpa.ItemTag];
nested exception is java.lang.IllegalArgumentException:
Unable to locate Attribute  with the the given name [note] on this ManagedType
[net.kaczmarzyk.spring.data.jpa.ItemTag]
```

So the third `@JoinFetch` is trying to fetch `note` off `ItemTag` (the type behind `tags`) instead of off `Orders`. It looks like once I've used the alias `o` once with `o.tags`, the next `o.<something>` no longer resolves back to the original `orders` join — it's resolving to whatever the previous `o.xxx` ended at.

If I only have two annotations (the alias-defining one plus one `o.xxx`) it works. The breakage shows up as soon as I add a second annotation that uses the same alias.

I'd expect the alias to keep pointing at the join I originally declared it for, so that every `@JoinFetch(paths = "o.xxx")` fetches `xxx` directly off `orders`, regardless of how many of them I chain.
