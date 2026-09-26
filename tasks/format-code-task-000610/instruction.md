## `fontVariant` style on `TextInput` is ignored

I'm using `TextInput` from react-native-paper and trying to apply a `fontVariant` (e.g. `small-caps` for a username field, or `tabular-nums` for an amount field). It works fine on a plain RN `<TextInput />` but has no visible effect when I apply it through paper's `TextInput`.

```tsx
import { TextInput } from 'react-native-paper';

<TextInput
  label="Amount"
  value={value}
  onChangeText={setValue}
  style={{ fontVariant: ['tabular-nums'] }}
/>
```

The text inside the input renders with the default glyphs as if `fontVariant` wasn't set at all. Other text style props on the same `style` object (like `fontSize` and `fontWeight`) do come through correctly, so it seems specific to `fontVariant`.

This happens with both `mode="flat"` and `mode="outlined"`, on both iOS and Android.

It would be great if `TextInput` respected `fontVariant` from `style` the same way it already respects the other font-related text styles.
