I'm passing a React element as `optionText` in `SelectInput`/`AutocompleteInput`, and that element uses `useRecordContext()`, but it doesn't get the current choice record and just renders blank. I thought I could reuse a Field-like component there, so I'm not sure if I'm configuring `optionText` wrong.

Expected outcomes:
- For `optionText` React elements in `<SelectInput>` and `<AutocompleteInput>`, components that call `useRecordContext()` should receive the current choice record while rendering each option.
- The same `optionText` React element behavior should apply consistently to `<AutocompleteArrayInput>`, `<SelectArrayInput>`, `<CheckboxGroupInput>`, `<RadioButtonGroupInput>`, and `<SelectField>`.
- React elements passed as `optionText` should no longer receive the current choice through an injected `record` prop; reusable Field-like components should access the choice through `useRecordContext()` instead.
- Existing supported non-element `optionText` forms, such as property names and rendering functions, should continue to render choices as before.

Implementation notes:
- Keep the public `optionText` API behavior consistent across the affected inputs and field component.
- The concrete component structure and where the context is provided are implementation details, as long as the rendered options expose the correct current choice through `useRecordContext()`.
- Avoid changing unrelated choice rendering semantics.
