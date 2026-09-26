RF02 false triggers on nested query in Trino dialect
### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

Consider the following SQL that includes a nested query in the FROM clause `SELECT id FROM foo`

```sql
SELECT
    a.id AS a_id,
    b.id AS b_id
FROM
    (
        SELECT id
        FROM foo
    ) AS a
JOIN bar AS b ON a.id = b.ib
```

Beginning in SQLFluff release 3.2.0 (and beyond to the latest 3.3.0 and current main branch) this fails with an RF02 violation. Version 3.1.1 and below does not. First screenshot is run from the 3.1.1 release. Second screenshot is run of the main branch pulled today.

![Image](https://github.com/user-attachments/assets/3c6f9145-2aa7-4a65-af26-af8769aa92a5)

![Image](https://github.com/user-attachments/assets/f35a00bf-5763-4e63-8898-e1aaa19600b3)

### Expected Behaviour

I expect this subquery to be allowed with the default RF02 rule because there is not more than one referenced table/view within the subquery, so the id column is unambiguous. Now there _is_ more than one referenced table within the outer query, but those are all aliased/referenced in an unambiguous way.

### Observed Behaviour

I'm seeing linting failures flagged as RF02 that don't seem to meet the definition of RF02, but only in subqueries.

### How to reproduce

Here's a script to make the example input and run it. It uses all default configuration.

```bash
# Create the SQL file
cat <<'EOF' > ./query.sql
SELECT
    a.id AS a_id,
    b.id AS b_id
FROM
    (
        SELECT id
        FROM foo
    ) AS a
JOIN bar AS b ON a.id = b.ib
EOF

# Run the linter
sqlfluff lint --dialect=trino ./query.sql
```

### Dialect

Trino

### Version

Raises RF02 Violation:
  * SQLFluff release 3.2.0
  * SQLFluff's main branch (today it's at 3527021)

No Violation:
  *  SQLFluff release 3.1.1

### Configuration

Default configuration - no customization.

### Are you willing to work on and submit a PR to address the issue?

- [x] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
