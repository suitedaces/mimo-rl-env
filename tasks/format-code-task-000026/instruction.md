Typescript: Wrong return type when using lean in different way
### Prerequisites

- [X] I have written a descriptive issue title
- [X] I have searched existing issues to ensure the bug has not already been reported


### Mongoose version

6.X.X - 7.X.X

### Node.js version

at least 16

### MongoDB server version

at least 4

### Typescript version (if applicable)

4.7 - latest

### Description

The return type of 

```ts
const a = await Model.findById('my-id', undefined, { lean: true })
```

is the same as

```ts
const a = await Model.findById('my-id')
```

it's:
```ts
// ^? const a: (mongoose.Document<unknown, {}, { name: string; }> & { name: string; } & { _id: mongoose.Types.ObjectId; }) | null
```


### Steps to Reproduce

See [ts playground](https://www.typescriptlang.org/play?ts=5.1.6#code/JYWwDg9gTgLgBCCA7A5hCBnApgGjgbwAKBlAYwAssQBDOAXzgDMoIQ4ByRVdbdgKD6lkGeBgpVaAXjhIsAdzhlKNABT4+cGdRBYAXARgBPMHsUwowVHihYAjgFdgNgCb7z9rHRx86ASgFCSCJwALIQzlgANnDSXGiYWAB0iBGRKuwAElGREOx4YsrU-oLC8FJw1HLUwPBhqYmMls4AQoYAks7p1Oz+1HwA9P1wAHoA-AGlcABGMRVVNaHhUQ1NrR1deXD2SBGNss54+HCRWNRIblAe9P5TA0NjE0HwpLOV1bVLkSs7a53s3b5Eiczip-KQ7iNRkA)

### Expected Behavior

The return type should be the same as

```ts
const a = await Model.findById('a').lean()
```

it's:

```ts
// ^? const a: (mongoose.FlattenMaps<{ name: string; }> & { _id: mongoose.Types.ObjectId; }) | null
```
