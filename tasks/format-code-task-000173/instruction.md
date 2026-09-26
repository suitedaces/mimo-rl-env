## Custom `dgs.graphql.graphiql.path` doesn't actually work end-to-end

I'm using the WebFlux variant of dgs-framework and I wanted to expose GraphiQL on a non-default path (we have a routing convention internally), so in my `application.yml` I set:

```yaml
dgs:
  graphql:
    graphiql:
      path: /my-graphiql
```

When I hit `/my-graphiql` in the browser it does redirect me to `/my-graphiql/index.html` like I'd expect, but the page that comes back is broken — GraphiQL loads but as soon as I try to run any query nothing happens, the requests don't go to my actual GraphQL endpoint. It's basically unusable on a custom path.

If I revert the config and go back to the default path everything works fine, so this only happens when I change `dgs.graphql.graphiql.path` to something other than the default.

My expectation is that this property should fully control where GraphiQL lives — not just the redirect, but the actual page being served at that path should also work correctly and talk to the configured GraphQL endpoint. Right now it feels like only part of the path config is being honored.
