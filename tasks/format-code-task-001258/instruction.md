Moto's dynamodb2 currently doesn't throw an error for this situation, where as the real dynamodb does.

For a query like so:

```python
table.update_item(
  Key={...},
  UpdateExpression='ADD x :one SET a = :a ADD y :one',
  ExpressionAttributeValues={':one': 1, ':a': 'lore ipsum'},
)
```

the real dynamo will return the error:

```txt
An error occurred (ValidationException) when calling the UpdateItem operation: Invalid UpdateExpression: The "ADD" section can only be used once in an update expression;
```

Whereas moto will happily process the query.
