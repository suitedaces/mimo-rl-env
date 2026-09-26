If the GraphQL query has validation errors such as variables not being used, or referencing unknown fragments, normally a GraphQL server can respond with a 400 status and a JSON response containing the GraphQL errors.

Unfortunately the GraphQL query complexity validator errors if the GraphQL query has validation issues, causing a 500 response that doesn't contain the detailed GraphQL errors. Ideally the complexity analysis would account for the possibility the query is invalid, and not cause an exception so that the normal GraphQL query validation errors can be reported.

Example correct 400 response for an invalid query:

```json
{
  "errors": [
    {
      "message": "Unknown fragment \"galleryExhibitConnection\".",
      "locations": [{ "line": 1, "column": 1532 }]
    },
    {
      "message": "Variable \"$devicePixelRatio\" is never used.",
      "locations": [{ "line": 1, "column": 623 }]
    },
    {
      "message": "Variable \"$cardPaginationLimit\" is never used.",
      "locations": [{ "line": 1, "column": 648 }]
    },
    {
      "message": "Variable \"$cardExhibitImageWidth\" is never used.",
      "locations": [{ "line": 1, "column": 757 }]
    },
    {
      "message": "Variable \"$cardExhibitImageHeight\" is never used.",
      "locations": [{ "line": 1, "column": 785 }]
    },
    {
      "message": "Variable \"$galleryExhibitsPageCursor\" is never used.",
      "locations": [{ "line": 1, "column": 894 }]
    },
    {
      "message": "Fragment \"GalleryExhibits_GalleryExhibitConnection\" is never used.",
      "locations": [{ "line": 1, "column": 1 }]
    }
  ]
}
```

With query complexity setup, the actual response has a 500 status without the GraphQL errors:

```json
{
  "errors": [{ "message": "Internal Server Error" }]
}
```

Here is the error logged in the server:

```
TypeError: Cannot read property 'typeCondition' of undefined
    at /[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:155:118
    at Array.reduce (<anonymous>)
    at QueryComplexity.nodeComplexity (/[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:88:75)
    at /[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:129:52
    at Array.reduce (<anonymous>)
    at QueryComplexity.nodeComplexity (/[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:88:75)
    at /[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:172:53
    at Array.reduce (<anonymous>)
    at QueryComplexity.nodeComplexity (/[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:88:75)
    at /[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:129:52
    at Array.reduce (<anonymous>)
    at QueryComplexity.nodeComplexity (/[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:88:75)
    at QueryComplexity.onOperationDefinitionEnter (/[redacted]/node_modules/graphql-query-complexity/dist/QueryComplexity.js:50:41)
    at Object.enter (/[redacted]/node_modules/graphql/language/visitor.js:323:29)
    at Object.enter (/[redacted]/node_modules/graphql/utilities/TypeInfo.js:370:25)
    at visit (/[redacted]/node_modules/graphql/language/visitor.js:243:26)
```

I'm using [`graphql-api-koa`](https://github.com/jaydenseric/graphql-api-koa), but I don't think that's relevant as it's GraphQL.js based.
