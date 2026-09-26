Comparison with empty string throws Invalid query: NO_COLUMN: null
**Describe the bug**
Comparison with empty string throws Invalid query: NO_COLUMN: null (at least for Google Sheets sources)

**To Reproduce**
Take the query from the README:

```
SELECT country, SUM(cnt)
FROM "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/edit#gid=0"
WHERE cnt > 0
GROUP BY country
```

Add a comparison with empty string:

```
SELECT country, SUM(cnt)
FROM "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/edit#gid=0"
WHERE cnt > 0 AND country != ''
GROUP BY country
```

Raises:

```
ProgrammingError: (shillelagh.exceptions.ProgrammingError) Invalid query: NO_COLUMN: null
```
