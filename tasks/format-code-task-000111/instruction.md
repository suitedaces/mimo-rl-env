## DatePicker crashes when used with a customInput that doesn't pass a standard event

I'm using `<DatePicker>` with a `customInput` (a wrapper input component from another UI lib). When the user types into it, that component fires its `onChange`, but the object it passes isn't a regular React SyntheticEvent — it's a plainer object that doesn't carry every method a native event has.

As soon as I type a character, the datepicker blows up inside `handleChange`. I traced it down to react-datepicker calling something on the event object that isn't there on what my customInput hands over.

Repro shape (roughly):

```jsx
const MyInput = React.forwardRef((props, ref) => (
  <SomeLibInput
    ref={ref}
    onChange={(value) => props.onChange({ target: { value } })}
    {...props}
  />
));

<DatePicker
  selected={date}
  onChange={setDate}
  customInput={<MyInput />}
/>
```

The `{ target: { value } }` object is enough for me to read what the user typed, but react-datepicker treats it like a full SyntheticEvent and breaks on it.

I'd expect `handleChange` to be defensive about what the underlying input hands it — if the argument isn't a "real" event, it should just keep going instead of crashing. The native-input case obviously still has to keep working as before.

Separately, while looking into this I noticed `onChangeRaw` only ever receives the first argument that the input passed in. Some inputs invoke `onChange(value, meta)` style and those extra arguments are silently dropped before reaching my `onChangeRaw` handler. It'd be nice if whatever the input calls `onChange` with gets forwarded through to `onChangeRaw` intact.
