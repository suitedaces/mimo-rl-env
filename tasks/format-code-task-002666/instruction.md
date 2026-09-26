## `@Builder(className = ...)` can't reference the target class name when used in a meta-annotation

I'm using Jilt with the meta-annotation feature — I define my own annotation, put `@Builder` on it with my preferred settings, and then sprinkle that meta-annotation around the codebase. Works great for things like `setterPrefix`, `buildMethod`, etc.

But I'm stuck when it comes to `className`. Something like:

```java
import org.jilt.Builder;

@Builder(className = "MyJiltBuilder")
public @interface MyBuilder {
}
```

If I use `@MyBuilder` on more than one class, every one of them ends up trying to generate a Builder called `MyJiltBuilder`, which obviously blows up — duplicate class name, doesn't compile. The only way to make it work today is to either leave `className` empty (which gives me the default `<TargetClass>Builder` and no way to customize it further), or to not use a meta-annotation at all and repeat `@Builder(className = "...")` per target with a different literal each time, which defeats the whole point of having the meta-annotation.

What I'd really want is for `className` to be able to incorporate the target class's name, so that e.g. building a `Person` gives me one name, building an `Order` gives me another, but the formatting (suffix/prefix/etc.) stays defined in one place on my meta-annotation.

Note that `@BuilderInterfaces.innerNames` already supports exactly this kind of "templated" name when used on a meta-annotation, so it's a bit surprising `className` doesn't. It would be nice if these two attributes behaved consistently.
