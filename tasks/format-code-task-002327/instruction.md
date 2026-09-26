MDX parser cannot parse HTML and React components in table cells
**Prettier 1.15.3**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEcAeAHCAnGACSKAZ3wCEIAbAEzwF48AKYMACwEtrsEBfASjoB8AHShCYAHhLZoAcwHN2nHuID0U2cNFQAxNrwBZACIANPDACGAIwpw8AdzYwWeABIAVfQBkRIgD54AYUoAVwBbKDwARjx-IIowiIAmGL8AWnTfdNTfPzw3dHx-SRhpKDl8tAk1Eo0UrV0DEzMrG3tHZwAlOHMwfEhQrCgEGB8oWJDwqJjAiaS6zIysnLG8gunxcmoBCqrNqgE6vDwRYtK5eErVdTLNEQuRiOOoDcp9+9U926HMHHwqOAAZuZghR8ExWBwqFwoHxBHhJHBemxoPIIUoYVdETBkVBNCAADQgCAYbHQIjIUDmbDSOwABSpCHJKHMADcIGwqASQJZsD0ANZwGAAZQwPTYZWQJWCcEJLBgoQoAHV2PAiKKwHAhYzHGwWY4AJ7IcBEcmE8VEOC4Wm8mShczIIEUC2EgBWRDQpF5YAFwvMoTgnnFcAd5idMpAbrQQvFMhsAEVghB4CGw4TRdgLdgjaEqGguRhsOKYIqOU5kAAOAAMaekFsVvIwRoLcEzLODhK4AEdgmwuNbzLb7UhHc6QBbQmwU6OiDH44nk0gpeGLJYS1Qy0hEoSSuYODGgqE7UaoNB2yBgha3FYmSO4NxuEA)
```sh
--parser mdx
--no-semi
--single-quote
```

**Input:**
```mdx
export const Bold = ({children}) =>
	<strong>{children}</strong>

## MDX table with HTML

| Column 1 | Column 2 |
|---|---|
| Text | <strong>Text</strong> |

## MDX table with React component

| Column 1 | Column 2 |
|---|---|
| Text | <Bold>Text</Bold> |
  
<strong>text</strong>

text
  
<Bold>text</Bold>

export default ({children}) => <section>{children}</section>

```

**Output:**
```mdx
SyntaxError: Unexpected token (1:9)
> 1 | <strong>
    |         ^
```

**Expected behavior:**

MDX tables should be able to contain HTML or React components in the table cells.

If you remove the HTML or React component from the cell, it will parse correctly.

HTML in table cells does seem to work with the `markdown` parser, so it seems to be an `mdx` parser issue.
