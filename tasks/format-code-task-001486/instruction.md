Template error with partial template in variable
### The problem

The following script generates an error instead of properly escaping the message:

```yaml
alias: Template Error in Variables
sequence:
  - variables:
      partial_template: "{{ '{%' ~ ' set value = ' }}"
  - service: notify.system_error_devices
    data:
      title: Template error example
      message: "{{ partial_template }}"
mode: single
```

### What version of Home Assistant Core has the issue?

core-2024.1.6

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

_No response_

### Link to integration documentation on our website

_No response_

### Diagnostics information

_No response_

### Example YAML snippet

```yaml
alias: Template Error in Variables
sequence:
  - variables:
      partial_template: "{{ '{%' ~ ' set value = ' }}"
  - service: notify.system_error_devices
    data:
      title: Template error example
      message: "{{ partial_template }}"
mode: single
```


### Anything in the logs that might be useful for us?

```txt
Stopped because an error was encountered at February 4, 2024 at 4:00:21 PM (runtime: 0.02 seconds)

invalid template (TemplateSyntaxError: unexpected 'end of template') for dictionary value @ data['message']
```
```


### Additional information

_No response_
