Support string initialization for map in schema
### Prerequisites

- [X] I have written a descriptive issue title
- [X] I have searched existing issues to ensure the feature has not already been requested


### 🚀 Feature Proposal

My project uses String for setting the type in schema of each keys like this:
```js
username: { type: 'string', required: true }
```

In case of map, I just tried this style of code:
```js
instance: {
  type: Schema.Types.Map,
  of: Schema.Types.Mixed,
  default: new Map<string, any>(),
}
```
This is working code. But if I use 'Map' instead of `Schema.Types.Map`, compiler aborts to compile.
```js
instance: {
  type: 'Map',
  of: 'Mixed',
  default: new Map<string, any>(),
}
```

So, is it able to allow with setting the map type with String?

### Motivation

_No response_

### Example

_No response_
