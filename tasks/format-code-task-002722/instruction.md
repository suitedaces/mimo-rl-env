False positive result for references.qualification with inner statement
### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

If I have a query with an inner select statement, then there is a wrong alert for references.qualification.

This is a regression, as it worked correctly in version 3.1.0.

### Expected Behaviour

Also in inner select statements with just one referenced table, an unqualifier reference should be accepted.

### Observed Behaviour

For inner select statements with one references table, the alert is raised

### How to reproduce

Create file `test.sql`
```
SELECT *
FROM (SELECT a FROM table)
```
and run ` sqlfluff lint test.sql -r rf02`
This throws
```
L:   2 | P:  14 | RF02 | Unqualified reference 'a' found in select with more than
                       | one referenced table/view.
                       | [references.qualification]
```

### Dialect

postgres

### Version

3.2.0

### Configuration

[sqlfluff]
dialect = postgres


### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
