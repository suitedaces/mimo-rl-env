### Description

Currently the oracle hook it not setting a CURRENT_SCHEMA after connecting with the Database.
In a lot of use cases we have production and test databases with seperate connections and database schemas e.g. TEST.Table1, PROD.Table1
"Hard-coding" the database schema in SQL Scripts is not elegant due to having different Airflow Instances for developing and Production.

An Option would be to store the database schema in a airflow Variable and getting it into the sql script with JINJA.
In Large SQL files with several tables it is not elegant either, because for every table a query to the metadatabase is made.

Why not using the Schema parameter in the Airflow Connections and executing 
`ALTER SESSION SET CURRENT_SCHEMA='SCHEMA'`
right after successfully connecting to the database?

An alternative would be to use option `Connection.current_schema ` of Library cx_Oracle.
https://cx-oracle.readthedocs.io/en/6.4.1/connection.html#Connection.current_schema



### Use case/motivation

It makes Query development much easier by storing environment attributes directly in the Airflow Connection.
You have full flexibility without touching your SQL Script.
It makes separation of Test and Production environments and connections possible.



### Related issues

_No response_

### Are you willing to submit a PR?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/apache/airflow/blob/main/CODE_OF_CONDUCT.md)
