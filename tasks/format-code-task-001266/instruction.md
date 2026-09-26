bool flag caused a panic
## Describe the bug
I passed an empty bool flag to a mixin and it caused a panic when it executed. 

## To Reproduce

```yaml
- az:
      description: "Remove application's resource group"
      arguments:
        - group
        - delete
      flags:
        name: "{{ bundle.parameters.resource-group }}"
        yes:
```

This also panics:

```yaml
      yes: ""
```

## Expected behavior
Definitely not a panic, at least an error if I should have used different formatting. Ideally it should pass my flag appropriately, e.g. `--yes`.

## Porter Command and Output
```
porter uninstall
```

## Version
porter v0.27.2 (aee93e98)

The code on this line used to use `fmt.Sprintf("%v"....)` shenanigans [here](https://github.com/deislabs/porter/blob/main/pkg/exec/builder/flags.go#L89) to convert the key to a string to avoid yaml's typing of keys as int and bools. What's happening is that yaml is interpreting "yes" or "y" as a bool, not a string. I was able to force it to a string in the yaml by changing it to

```yaml
    "yes":
```

We should go back to the old hack and comment why it's there with a test so that I'm not tempted to remove it again. 😊
