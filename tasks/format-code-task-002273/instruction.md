## Column name for `SELECT NULL` and string literals doesn't match MySQL

I'm using TiDB as a drop-in MySQL replacement for an app that relies on the column names returned by simple literal SELECTs (we use them as map keys downstream). When I started comparing TiDB's output against MySQL's, the column names for literal expressions don't line up.

### Reproduction

Connect to TiDB and run:

```sql
SELECT NULL;
SELECT 'a';
SELECT '   hello';
```

Then run the same statements against MySQL 5.7 and look at the column name reported in the result set metadata (i.e. the header you see in the `mysql` CLI, or what a client library reports as the field name).

### What I see in MySQL

```
mysql> SELECT NULL;
+------+
| NULL |
+------+
| NULL |
+------+

mysql> SELECT 'a';
+---+
| a |
+---+
| a |
+---+

mysql> SELECT '   hello';
+-------+
| hello |
+-------+
| hello |
+-------+
```

The column name is the literal value itself — `NULL` for a NULL literal, and the string content for a string literal (with leading whitespace/non-printable characters trimmed).

### What I see in TiDB

The column names I get back for the same statements don't match — `SELECT NULL` and `SELECT 'a'` come back with something else in the field name, which breaks the code that's keying off the column header.

### Expected

For consistency with MySQL, when a SELECT field is a bare literal (no alias, no expression around it):

- A NULL literal should produce the column name `NULL`.
- A string literal should produce the column name equal to the string's content.

Other literal kinds (numeric, etc.) and non-literal expressions already look fine to me — it's specifically the NULL and string-literal cases that are off. Would be great to align this with MySQL so existing MySQL clients/tools see the same field names.
