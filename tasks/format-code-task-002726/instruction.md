Postgres `ON` preventing formatting after occurrence.
### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

I note that any query that I have is not formatted correctly (in terms of indentation) after a `on conflict (..) do` statement.
Within the query, anything that is before the `on` is formatted absolutely perfectly, but after it fails to indent.


Example of SQL to format:
```
insert into foo (
id,
bar
)
values (
$1,
$2
) on conflict (id) do update
set
bar = $2;
```

### Expected Behaviour

(I think I should expect this - at least, just any indentation after the `do`...)
```
insert into foo (
    id,
    bar
)
values (
    $1,
    $2
)
on conflict (id) do update
    set
        bar = $2;
```


If I have just a `update` statement (without a `do`) it indents as follows just fine.
```
update foo
set
bar = $2;
```
is converted to
```
update foo
set
    bar = $2;
```

### Observed Behaviour

Any query that I have is indented absolutely fine until a `on conflict ... do update` is reached.
Running `fix` on the above yields:

```
insert into foo (
    id,
    bar
)
values (
    $1,
    $2
)
on conflict (id) do update
set
bar = $2;
```

### How to reproduce

Here is some example SQL that will fail to indent after `on conflict .. do update` 


```
insert into foo (
    id,
    bar
)
values (
    $1,
    $2
)
on conflict (id) do update
set
bar = $2;
```

### Dialect

Postgres

### Version

sqlfluff, version 3.3.1

### Configuration

[.sqlfluff](https://github.com/user-attachments/files/18827374/sqlfluff.txt)

### Are you willing to work on and submit a PR to address the issue?

- [x] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)
