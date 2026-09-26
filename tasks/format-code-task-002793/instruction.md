## Nested input types: inner fields are treated as output types

I'm defining a GraphQL config where a mutation takes an input type, and that input type has a field whose type is *another* input type (i.e. nested input types). Something like:

```graphql
type Mutation {
  createPost(input: PostInput!): Post
}

input PostInput {
  title: String!
  author: AuthorInput!   # <-- inner field references another input type
}

input AuthorInput {
  name: String!
}

type Post {
  title: String!
}
```

When tailcall processes this config, the inner input type (`AuthorInput` in the example above) doesn't behave as an input type. It seems to get classified as an output type instead, which then breaks downstream schema handling — the generated SDL / type categorization is wrong for any input type that's only reachable transitively through another input type's fields.

Only the input types directly referenced by a field's argument seem to be recognized as inputs. As soon as you go one level deeper (input referencing another input through a field), the deeper one is no longer treated as input.

Expected: every type reachable from an argument — including types referenced by fields of an input type, recursively — should be considered an input type, not an output type. Whether a type is "input" shouldn't depend on whether it happens to be referenced directly by an arg or transitively through another input.
