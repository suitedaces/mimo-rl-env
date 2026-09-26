The remove-x-internal decorator doesn't remove references to x-internal components
Let's say we're referencing two parameter components, one internal:
```
      parameters:
        - $ref: '#/components/parameters/ProductID'
        - $ref: '#/components/parameters/Vendor'
```
```
  parameters:
    ProductID:
      in: path
      name: product_id
      description: The ID of the product.
      required: true
      schema:
        type: string
        format: uuid
    Vendor:
      in: header
      name: X-Vendor
      description: The vendor.
      schema:
        type: string
      x-internal: true
```

Once we run the remove-x-internal decorator, the Vendor component will be removed, but the reference to it will remain. Perhaps because the order of the removals is wrong (we remove the component then check the reference?)

Full repro: https://github.com/bojanz/openapi-cli-bug/tree/builtin-decorator
