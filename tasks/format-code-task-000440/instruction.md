## CloudFormation `Condition:` references don't seem to be evaluated

I'm scanning a CloudFormation template that uses the top-level `Conditions:` block, and several places in the template reference those conditions by name. The references don't appear to take effect during scanning — it's as if the condition is never actually evaluated.

Minimal template that shows the problem:

```yaml
Parameters:
  Env:
    Type: String
    Default: prod

Conditions:
  IsProd: !Equals [!Ref Env, "prod"]

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !If
        - IsProd
        - prod-bucket
        - dev-bucket

Outputs:
  MaybeArn:
    Condition: IsProd
    Value: !GetAtt MyBucket.Arn
```

With `Env=prod` I'd expect `IsProd` to evaluate to true, so:

- the `!If` should pick the `prod-bucket` branch, and
- the `MaybeArn` output (gated by `Condition: IsProd`) should be present.

When I scan this, the behaviour I see downstream doesn't match either expectation — it looks like the `Condition: IsProd` reference in the output, and condition references in general, are not being resolved against the `Conditions:` block at all. Plain things like `!Equals`, `!Ref` on parameters, etc. seem fine on their own; it's specifically the by-name reference to a declared condition that doesn't seem to do anything.

Both forms of the reference should work — the long form:

```yaml
Outputs:
  MaybeArn:
    Condition: IsProd
    Value: ...
```

and the YAML short-tag form:

```yaml
SomeValue: !Condition IsProd
```

It would be great if these references were actually resolved to the value of the named condition from the `Conditions:` block, so that anything depending on them (If branches, conditional outputs, etc.) behaves the way the template intends.
