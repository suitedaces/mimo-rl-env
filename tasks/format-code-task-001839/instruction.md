expression migrator generates invalid style if icon-image value is a categorical function
**mapbox-gl-js version**: latest 1.x.x

**browser**: N/A

### Steps to Trigger Behavior

1. Attempt to migrate a style that uses a categorical function on the text-image field.
2. See validation error.

### Link to Demonstration

https://github.com/mapbox/mapbox-gl-js/pull/10055

### Expected Behavior

Migrated style is valid. I see two ways to fix this problem:

1. Make migrator insert an empty string as fallback value for icon-image when migrating categorical expression.
2. Make GL JS support undefined values for icon-image.

I can take care of fixing this if someone on GL JS has a preferred approach between those two. I'm thinking using an empty string as fallback is the best option. This can be fixed by adjusting the logic around categorical conversion for `image` type values: https://github.com/mapbox/mapbox-gl-js/blob/ff8e087b6e7cc9fe63eb4809a0895b38029a67e2/src/style-spec/function/convert.js#L140 – this line can resolve to undefined, leading to an invalid style.

### Actual Behavior

Migrated style is not valid. 

```
// Input
{
  base: 1,
  type: 'categorical',
  property: 'type',
  stops: [['park', 'some-icon']]
}
```

```
// Output
[ 'match', [ 'get', 'type' ], 'park', 'some-icon', undefined ]
```

Error: "layers[0].layout.icon-image[4]: 'undefined' value invalid. Use null instead."
