.throwOnError() doesn't do typecheck
# Bug report

## Describe the bug

From my understaning of https://github.com/supabase/supabase-js/issues/92 `.throwOnError()` should work as if I were typing something like:
```ts
	const { data: queryResult, error: queryError } = await supabase
		.from("cohorts")
		.select("id")
		.single();

	if (queryError) {
		throw queryError;
	}
	const thisHasTypeId = queryResult; // This is of type { id: number } NOT NULL!!
```
In the above case `thisHasTypeId` is of type `{id:number}`, but if I try to use `.throwOnError()`:
```ts
	const { data: queryResult, error: queryError } = await supabase
		.from("cohorts")
		.select("id")
		.single()
		.throwOnError();


	const thisHasTypeNullToo = queryResult; // This is of type { id: number } | null, WHY NULL??
```
But here `thisHasTypeNullToo` has null too! so I would have to do type check as well like this:
```ts
	const { data: queryResult, error: queryError } = await supabase
		.from("cohorts")
		.select("id")
		.single()
		.throwOnError();


	const thisHasTypeNullToo = queryResult; // This is of type { id: number } | null, WHY NULL??

	if (queryError) {
		throw queryError;
	}
	const thisDoesNotHaveTypeNull = queryResult; // This is of type { id: number } NOT NULL!!

```

## Expected behavior

It would be nice if the returned `data` didn't include the `null` type when using .throwOnError().
