This isn't an issue with `go-logr` but it may be worth identifying as a potential trap for the unwary; I *will* update my blog [post](https://pretired.dazwilkin.com/posts/211018/).

My naive implementation of `RenderValuesHook` was:

```golang
renderLabels := func(kvList []interface{}) []interface{} {
  // loggingLabels becomes the only label key
  return []interface{}{
    loggingLabels,
    funcr.PseudoStruct(kvList),
  }
}
```

This worked fine if `WithValues` is only called once per Logger. If `WithValues` is called again, the existing labels are nested within the new set, i.e.:

```JSON
{
  "jsonPayload": {
    "logging.googleapis.com/labels": {
      "logging.googleapis.com/labels": { <--- INCORRECT
        "foo": "X"
      },
      "bar": "Y"
    }
  }
  "labels": {
    "instanceId": "00bf4bf0..."
  }
}
``` 

> **NOTE** In my case, Google Cloud Logging no longer recognized the borked `logging.googleapis.com/labels` as special values and does not merge them with the `labels` field.

Using [`NewStdoutLogger`](https://github.com/go-logr/logr/blob/8d00e357f1cbbb9246ed8bbf03f2c8fe242d2ae9/example_test.go#L27), the issue does not occur:

```Golang
	l := NewStdoutLogger()
	l.Info("info")

	l = l.WithValues("foo", "X")
	l.Info("info")

	l = l.WithValues("bar", "Y")
	l.Info("info")
```
Outputs:

```console
"level"=0 "msg"="info"
"level"=0 "msg"="info" "foo"="X"
"level"=0 "msg"="info" "foo"="X" "bar"="Y"
```

So, it's an issue with my implementation.

I revised the implementation (improvements welcome):

```golang
renderLabels := func(kvList []interface{}) []interface{} {
  // If loggingLabels is present, it will be the first label key
  k, _ := kvList[0].(string)
  if k == loggingLabels && len(kvList) > 2 {
    // The label values should be a PseudoStruct
    v, _ := kvList[1].(funcr.PseudoStruct)
    // Append additional ([2:]) label keys|values to the existing loggingLabels
    // loggingLabels becomes the only label key
      return []interface{}{
        loggingLabels,
        append(v, funcr.PseudoStruct(kvList[2:])...),
      }
    }

    // loggingLabels becomes the only label key
    return []interface{}{
      loggingLabels,
      funcr.PseudoStruct(kvList),
    }
}
```

And, replacing `NewStdoutLogger` with `NewStructuredLogger`, I get:

```console
{"level":0,"msg":"info"}
{"level":0,"msg":"info","logging.googleapis.com/labels":{"foo":"X"}}
{"level":0,"msg":"info","logging.googleapis.com/labels":{"foo":"X","bar":"Y"}}
```
