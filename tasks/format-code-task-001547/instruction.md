Support react-i18next "defaults" prop
#### Version
- i18next: <i>11.2.2</i>
- i18next-scanner: <i>2.4.6</i>
- react-i18next: <i>7.7.0</i>

#### Configuration
```js
options: {
	// use strings as keys
	nsSeparator: false,
	keySeparator: false,
	// settings
	defaultNs: "frontend",
	lngs: ["en"],
	resource: {
		loadPath: "{{lng}}/{{ns}}.json",
		savePath: "{{lng}}/{{ns}}.json",
	},
	func: false,
	trans: false,
	defaultValue: (language, namespace, key) => key,
},
```

react-i18n v7.7.0 introduced the `defaults` prop (see i18next/react-i18next#439). I expect the following code:

```jsx
<Trans
  defaults="Hello <0>{val}</0>!"
  tOptions={{val: "World"}}
  components=[<strong>foo</strong>]
/>
```

to lead to the following output:

```json
{
  "Hello <0>{val}</0>!": "Hello <0>{val}</0>!"
}
```
