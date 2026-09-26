Support duckdb's asof join syntax
**Is your feature request related to a problem? Please describe.**

Not related to a problem.

**Describe the solution you'd like**

I'd like this query to be parsable by sqlglot:

```
SELECT s.*, p.unit_price, s.quantity * p.unit_price AS total_cost
  FROM sales s ASOF LEFT JOIN prices p
    ON s.sale_time >= p.ticker_time
```

Here's the syntax diagram for `FROM`, which includes the allowed asof join syntax:

![image](https://github.com/tobymao/sqlglot/assets/417981/8bd91cca-5c3f-4bd8-8cad-7c0c11f07058)

**Describe alternatives you've considered**

I haven't considered any alternatives other than I guess this feature continuing to not exist.
