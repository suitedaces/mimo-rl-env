## Searching for queries

Our team has accumulated quite a lot of saved queries in Redash, and the `/queries` page is becoming hard to navigate. Right now it just lists all the queries with the table's built-in filter on top, which is fine when you have a handful, but doesn't really help once the list gets long — it only filters whatever the current page is showing.

A few situations where this becomes painful:

- I'm trying to find a query I wrote a while back and only remember a keyword from its name.
- I want to check whether someone else on the team has already written a query about some particular metric / table / business concept. The query *name* doesn't always make this obvious, but it's often spelled out in the description.
- I'm in the middle of working on a dashboard or another query, and I just want to jump to a related query without having to navigate away to the full list and scroll around.

It would be really useful to have actual search for queries — type a keyword, get back the queries that match (against the query name and the description, since both are useful). And ideally I shouldn't have to be on the queries list page first to use it; it would be nice to be able to kick off a search from wherever I happen to be in the app.
