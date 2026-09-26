# Let Airflow operator parameters consume outputs from parent nodes

Right now, when we parse an Apache Airflow operator into a component, every parameter we
surface in the pipeline editor is locked to a single input control matching the parameter's
detected type (a text box for strings, a checkbox for booleans, a number field for numbers,
and so on). The only thing a user can do is type a literal value.

We want Airflow operators to be able to exchange data: any operator parameter should *also*
be able to receive, as its value, an output produced by one of its parent nodes in the
pipeline. The editor already knows how to render a "pick one of several input types" control,
so what's missing is that our parsed Airflow components need to describe each parameter as a
choice between **its native value control** and a control that lets the user **select an output
from a parent node**.

Concretely, the canvas properties we generate for an Airflow component
(`ComponentCatalog.to_canvas_properties(component)`) must change for every parsed operator
parameter (the synthetic `label` and `component_source` fields must stay exactly as they are
today and must not be turned into this new structure).

For each operator parameter, the `uihints.parameter_info` entry must look like:

```jsonc
{
  "parameter_ref": "elyra_<param>",
  "control": "custom",
  "custom_control_id": "OneOfControl",
  ...
  "data": {
    "controls": {
      "<NativeControl>":   { "label": "<some label>", "format": "<the parameter's data type>" },
      "NestedEnumControl": { "label": "<some label>", "format": "inputpath", "allownooptions": false }
    },
    "required": <bool>
  }
}
```

where:

- `custom_control_id` is `"OneOfControl"` for every operator parameter.
- `data.controls` holds **exactly two** entries:
  - `"NestedEnumControl"` — the option to consume a parent node's output. Its `format` is
    `"inputpath"` and it carries `"allownooptions": false`.
  - the parameter's **native control** — `"NumberControl"` for numeric parameters,
    `"BooleanControl"` for boolean parameters, and `"StringControl"` for everything else
    (strings, dictionaries, lists, undetermined types). Its `format` is the parameter's
    detected data type (e.g. `"string"`, `"number"`, `"boolean"`, `"dictionary"`, `"list"`).
  - each control entry includes a non-empty human-readable `"label"` string.
- `data.required` is a boolean: a parameter is **required** when the operator's `__init__`
  argument has no default value, and **optional** when it does.

The matching `current_parameters` entry for each operator parameter must become an object that
records which control is initially active and stores the parameter's default value under that
control:

```jsonc
"elyra_<param>": {
  "activeControl": "<NativeControl>",
  "<NativeControl>": <the same default value we produce today>
}
```

The initially active control is the parameter's native control, and the value stored under it
is the parameter's default value as it is determined today (`''` for a string with no default,
the parsed default otherwise; `false`/`true` for booleans; the integer for numbers; etc.).

Components for other runtimes (e.g. Kubeflow Pipelines) must be unaffected — their parameters
should keep their single native control and their flat `data.format`/scalar
`current_parameters` values.

The rendered properties must remain valid JSON.
