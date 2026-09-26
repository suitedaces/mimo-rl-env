## Custom fields on `Query` type lose the auto-generated query arguments

I'm using `makeAugmentedSchema` and would like to mix the auto-generated CRUD API with a few of my own query fields (custom resolvers, alternate entry points, etc.). The problem is that when I declare my own `Query` type in the SDL, my custom fields don't receive the standard query arguments (`first`, `offset`, `filter`, `orderBy`) even when they return a node type that otherwise gets them on the auto-generated query field.

Minimal example:

```js
const typeDefs = `
  type Movie {
    movieId: ID!
    title: String
    year: Int
  }

  type Query {
    moviesByYear(year: Int!): [Movie]
  }
`;

const schema = makeAugmentedSchema({ typeDefs });
```

After augmentation:

- The auto-generated `Query.Movie(...)` field has all the expected args: `first`, `offset`, `filter: _MovieFilter`, `orderBy: [_MovieOrdering]`, etc.
- My `Query.moviesByYear(year: Int!): [Movie]` field only has `year` — none of the standard pagination / filtering / ordering args were added, even though it returns `[Movie]`.

I'd expect any user-defined query field whose return type is an augmented node type to get the same standard argument set as the generated query field for that node type. Otherwise there's no way to add a custom query entry point that participates in the normal filtering / paging API — I have to choose between "let the lib generate everything" and "give up filter/orderBy entirely on my custom field".

Same situation seems to apply if the field is defined via a schema extension on `Query`.

Could the augmentation be extended so that fields on a user-declared `Query` type are processed the same way as auto-generated ones (i.e. node-typed return values get the standard query arguments + the related filter/ordering input types referenced)?

While I'm at it — passing a partial config also bites: e.g. `config: { query: true, mutation: true }` (no `temporal` / `spatial` keys) behaves differently from omitting `config` entirely. It would be nice if missing config keys fell back to a sensible default rather than being treated as "disabled".
