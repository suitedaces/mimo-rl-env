Unable to parse snowflake 'unset comment' command
### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

When we tried parsing the below command using sqlfluff, there has been a parsing error. Same command runs on snowflake without any issue.
ALTER TABLE SAMPLE_DB.SAMPLE_SCHEMA.TABLE UNSET COMMENT;

### Expected Behaviour

command should be parsed correctly

### Observed Behaviour

=========================== short test summary info ============================
FAILED tests/test_sqdbm_config.py::test - AssertionError: \n**Parsing failed**\nErrors found in files:\nmigrations//test.sql:
  ==== parsing violations ====
  L:   2 | P:   1 |  PRS | Line 2, Position 1: Found unparsable section: 'ALTER TABLE
                         | SAMPLE_DB.SAMPLE_SCHEMA.TABLE UNSET...'
  WARNING: Parsing errors found and dialect is set to 'snowflake'. Have you configured your dialect correctly?

### How to reproduce

run the below command

sqlfluff parse test.sql --dialect snowflake --config=tests/config.sqlfluff

### Dialect

snowflake

### Version

2.3.5

### Configuration

```
[sqlfluff]
#exclude_rules = LT01, LT02, LT03, LT04, LT05, LT06, LT07, LT08, LT09, LT10, LT11, LT12, LT13, CP02, ST01, ST02, ST03, ST04, ST05, ST06, ST07, ST08, ST09, AM04, AL03, RF03, RF05, CP01, CP05, CP03, AL01, CV11, CV02
# layout rules are excluded
# Use the below link for rules code
# https://docs.sqlfluff.com/en/stable/rules.html
#large_file_skip_byte_limit = 0

```

### Are you willing to work on and submit a PR to address the issue?

- [X] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
