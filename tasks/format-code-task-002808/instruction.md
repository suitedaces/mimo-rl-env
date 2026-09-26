EventListener fails to create service due to max length limitation
### Feature request

When creating an EventListener with a long name, it fails to create the Service due to the max length limitation of 63 characters. Does it make sense to reject the creation of the event listener in the first place? Or are there other options available to handle this internally?

```
apiVersion: triggers.tekton.dev/v1alpha1
kind: EventListener
metadata:
  name: mkt-cloud---product-hierarchy-replication-salesbagsreplication
(...)
status:
  conditions:
  - lastTransitionTime: "2021-01-18T21:50:35Z"
    message: 'Service "el-mkt-cloud---product-hierarchy-replication-salesbagsreplication"
      is invalid: metadata.name: Invalid value: "el-mkt-cloud---product-hierarchy-replication-salesbagsreplication":
      must be no more than 63 characters'
    status: "False"
    type: Service
```

I´m currently using release v0.10.2.

Thanks, Fabian
