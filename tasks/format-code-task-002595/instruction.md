Support function-level hooks via `LazySchema`
```python
import schemathesis

schema = schemathesis.from_pytest_fixture("fixture_name")

def before_generate_query(context, strategy):
    return strategy.filter(lambda x: len(x["id"]) > 5)

@schema.hooks.apply(before_generate_query)
@schema.parametrize()
def test_api(case):
```
