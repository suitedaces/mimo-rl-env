I’m using `ngx-toggle` in a form and noticed that the form value changes, but my `(change)` handler on the component never runs, even when I click the toggle or update the bound model. Also, passing things like `disabled="false"` seems to still behave like it’s disabled, which feels off for Angular inputs. Could you make the toggle behave more like a normal Angular form control here, so `(change)` actually gives me the current boolean value and those basic inputs are interpreted correctly?

Expected outcomes:
- Change events: `ngx-toggle` should invoke its public `(change)` output when the toggle value changes through normal user interaction, and the emitted event value should be the current boolean toggle value.
- Form integration: when a bound form model or `ControlValueAccessor` write changes the toggle to a different value, the component should run the same observable change behavior so `(change)` subscribers receive the current value.
- Input coercion: the public `disabled` and `required` inputs should interpret common Angular boolean-style values correctly, including treating the string `"false"` as false.
- Numeric input coercion: the public `tabIndex` input should normalize numeric string values so the underlying checkbox receives a numeric tab index.
- Template references: `ngx-toggle` should be exportable in templates as `ngxToggle`, allowing usage such as a template reference to the component instance.

Implementation notes:
- Preserve `ngx-toggle` as a normal Angular form-control component and keep existing public bindings compatible unless the behavior above requires otherwise.
- The exact internal structure, helper methods, change-detection strategy, and validation locations are implementation details; choose whatever approach best supports the observable behavior.
