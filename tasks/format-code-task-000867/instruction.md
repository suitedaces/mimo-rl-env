Components disappear in certain cases.
In the `Sorting.js` container, we have the following code:

```
if (!searchTerm && results.length === 0) return null;
```

The intent of this code was to hide the Component on the initial load of the Search UI experience, and not show it until it is needed.

There are few issues with this.

1. Individual UI components should not be responsible for this. This is something that should happen at a top level IF it is needed. Not every user of the API will need this. Some users will not have an initial empty state.

2. The check itself is not actually successfully checking for the initial empty state of the UI. It is possible to get back into this case where you have 0 results with no search term by some creative use of filters.
