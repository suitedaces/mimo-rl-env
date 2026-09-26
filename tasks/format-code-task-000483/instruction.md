## Remove the required column list from `Automerge.Table`

When you create a table, you currently have to pass in a list of column names:

```js
doc.authors = new Automerge.Table(['surname', 'forename'])
doc.publications = new Automerge.Table(['type', 'authors', 'title', 'publisher', 'edition', 'year'])
```

But as far as I can tell, this list of columns isn't actually used for anything meaningful anymore. Since #236, you can no longer add a row by passing an array of values that gets mapped to column names — rows must already be objects with named properties. So the column list doesn't enforce a schema, doesn't validate row shapes, doesn't affect storage, and rows are free to omit some of the "columns" or include extra properties not in the list.

In other words, requiring this argument forces every user to write something that looks meaningful but isn't. It's confusing — new users reasonably assume the column list does something (enforces required fields, fixes a row shape, etc.) and then are surprised when it doesn't.

I think we should just drop the column list from the `Table` API. Creating a table should look like:

```js
doc.authors = new Automerge.Table()
doc.publications = new Automerge.Table()
```

Rows continue to be plain objects, and by convention users should give rows in the same table the same set of properties, but Automerge doesn't (and currently can't) enforce that. The docs should be updated to reflect this — and to mention that not enforcing a schema is actually somewhat intentional, since different clients in a collaborative app may be running different versions and using slightly different property sets.

If/when proper schema support is added later, that can be designed properly. The current half-feature isn't getting us closer to that and just adds noise to the API.

Thoughts?
