Support traversing scope within UPDATE statements.
**Is your feature request related to a problem? Please describe.**
`traverse_scope()` function does not handle SELECT statements within UPDATE statements. 
I was expecting couple of scopes form below example but it ignores any SELECTS within UPDATES.


```py

from sqlglot import Parser, exp, parse, parse_one
from sqlglot.optimizer.scope import traverse_scope

sql = """

UPDATE customers
SET total_spent = (
    SELECT SUM(amount)
    FROM payments
    WHERE payments.customer_id = customers.id
)
WHERE EXISTS (
    SELECT 1
    FROM payments
    WHERE payments.customer_id = customers.id
);
"""

parsed = parse_one(sql)
for scope in traverse_scope(parsed):
    print(scope)

```

**Describe the solution you'd like**
Any chance this can be fixed?

Thanks!
