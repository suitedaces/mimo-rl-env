## Generated clients still import `longrunningpb` / `iampb` from old `google.golang.org/genproto` paths

The `longrunningpb` and `iampb` proto stubs have been republished under new module paths:

- `google.golang.org/genproto/googleapis/longrunning` → `cloud.google.com/go/longrunning/autogen/longrunningpb`
- `google.golang.org/genproto/googleapis/iam/v1` → `cloud.google.com/go/iam/apiv1/iampb`

The generator itself has already been updated to consume these new packages internally. However, when I regenerate a client that uses the LRO mixin and the IAM policy mixin, the generated `*_client.go` files still emit imports like

```go
longrunningpb "google.golang.org/genproto/googleapis/longrunning"
iampb         "google.golang.org/genproto/googleapis/iam/v1"
```

and the generated example snippets still point users at the old documentation URLs, e.g.

```go
req := &longrunningpb.ListOperationsRequest{
    // TODO: Fill request struct fields.
    // See https://pkg.go.dev/google.golang.org/genproto/googleapis/longrunning#ListOperationsRequest.
}
```

```go
req := &iampb.SetIamPolicyRequest{
    // TODO: Fill request struct fields.
    // See https://pkg.go.dev/google.golang.org/genproto/googleapis/iam/v1#SetIamPolicyRequest.
}
```

That's inconsistent with where these stubs actually live now, and it means freshly generated clients pull in the old genproto package alongside whatever else they depend on.

Could the generator be updated so that anywhere it emits a reference to the longrunning or IAM v1 proto packages — both in real client code and in the `pkg.go.dev` links inside generated examples — it uses the new `cloud.google.com/go/...` paths instead?
