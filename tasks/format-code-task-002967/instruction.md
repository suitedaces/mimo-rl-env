## `vgl-extrude-geometry` doesn't actually accept any props

The `vgl-extrude-geometry` component is currently just a stub — its `inst` always returns `new ExtrudeBufferGeometry([], {})`, regardless of what I pass to it. So no matter what attributes I write on the tag, I always end up with an empty extruded geometry.

I'd like to actually use it. For example:

```html
<vgl-renderer>
  <vgl-scene>
    <vgl-mesh>
      <vgl-extrude-geometry
        :shapes="myShape"
        depth="20"
        bevel-enabled
        bevel-thickness="2"
        bevel-size="1"
        bevel-segments="3"
        steps="2"
        curve-segments="12"
      ></vgl-extrude-geometry>
      <vgl-mesh-basic-material color="red"></vgl-mesh-basic-material>
    </vgl-mesh>
  </vgl-scene>
  ...
</vgl-renderer>
```

Right now none of these attributes have any effect — the result is the same empty geometry as if I'd written `<vgl-extrude-geometry></vgl-extrude-geometry>`.

### What I'd expect

The component should expose the full configuration surface of [`THREE.ExtrudeBufferGeometry`](https://threejs.org/docs/#api/en/geometries/ExtrudeBufferGeometry) — the shape input, plus the options the constructor takes (depth, steps, curveSegments, all the bevel-* options, the optional extrude path, the UV generator, etc.). Updating any of these on the Vue side should reactively rebuild the geometry, like the other vue-gl geometry components do.

### Input forms for `shapes`

To stay consistent with the rest of vue-gl (where most props can be given either as a string, as a plain JS structure, or as the corresponding Three.js object), I'd like `shapes` to be flexible too. In particular I want all of the following to work for describing the 2D outline:

- a list of points where each point is a space-separated string like `"12 2"`
- a list of points where each point is a plain `[x, y]` number array
- a list of `THREE.Vector2` instances
- an actual `THREE.Shape` (or an array of `THREE.Shape`) passed via `:shapes="..."`

The second form (plain `[x, y]` number arrays) is what I really need — currently the existing vector2 parsing only handles strings and `Vector2` instances, so passing `[[12, 2], [10, 0], ...]` blows up. It would be nice to also support that shorthand wherever vector2 inputs are accepted.

Finally, the property-types doc page lists every prop type the framework parses — please add the new `shapes` type there so users know what shape of input is accepted.
