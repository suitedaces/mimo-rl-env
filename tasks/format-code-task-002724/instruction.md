DuckDB: MAP data type not supported
### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

```sql
CREATE TABLE map (tags MAP(VARCHAR, VARCHAR));
```

When `CREATE TABLE` statement with nested types are given SQLFluff fails to parse.

### Expected Behaviour

It should be successfully parsed.

### Observed Behaviour

The rest of SQL goes to unparsable section with error message: `Expected: "<Delimited: [<Ref: 'StatementSegment'>]>"`

### How to reproduce

```
echo 'CREATE TABLE map (tags MAP(VARCHAR, VARCHAR));' | sqlfluff parse -d duckdb -
[L:  1, P:  1]      |file:
[L:  1, P:  1]      |    unparsable:                                               !! Expected: "<Delimited: [<Ref: 'StatementSegment'>]>"
[L:  1, P:  1]      |        word:                                                 'CREATE'
[L:  1, P:  7]      |        whitespace:                                           ' '
[L:  1, P:  8]      |        word:                                                 'TABLE'
[L:  1, P: 13]      |        whitespace:                                           ' '
[L:  1, P: 14]      |        word:                                                 'map'
[L:  1, P: 17]      |        whitespace:                                           ' '
[L:  1, P: 18]      |        start_bracket:                                        '('
[L:  1, P: 19]      |        word:                                                 'tags'
[L:  1, P: 23]      |        whitespace:                                           ' '
[L:  1, P: 24]      |        word:                                                 'MAP'
[L:  1, P: 27]      |        start_bracket:                                        '('
[L:  1, P: 28]      |        word:                                                 'VARCHAR'
[L:  1, P: 35]      |        comma:                                                ','
[L:  1, P: 36]      |        whitespace:                                           ' '
[L:  1, P: 37]      |        word:                                                 'VARCHAR'
[L:  1, P: 44]      |        end_bracket:                                          ')'
[L:  1, P: 45]      |        end_bracket:                                          ')'
[L:  1, P: 46]      |        semicolon:                                            ';'
[L:  1, P: 47]      |    newline:                                                  '\n'
[L:  2, P:  1]      |    [META] end_of_file:

==== parsing violations ====
L:   1 | P:   1 |  PRS | Line 1, Position 1: Found unparsable section: 'CREATE TABLE map
                       | (tags MAP(VARCHAR, VARC...'
WARNING: Parsing errors found and dialect is set to 'duckdb'. Have you configured your dialect correctly?
```

### Dialect

DuckDB

### Version

sqlfluff, version 3.2.5

### Configuration

```ini
[sqlfluff]
dialect = duckdb
```

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
