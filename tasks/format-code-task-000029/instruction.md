## Statics that override built-in model/document methods are getting wrapped with hooks unexpectedly

I'm using a plugin similar to `mongoose-delete` that overrides some built-in methods (`save`, `remove`, etc.) by attaching them through `schema.statics`. My schema also defines normal hooks like `pre('save')` / `post('save')` for unrelated business logic on documents.

Roughly:

```js
const schema = new Schema({ name: String });

// plugin-style: override built-in via statics
schema.statics.save = function() { /* custom impl */ };

// my own business hook for document save
schema.pre('save', function() { /* ... */ });
schema.post('save', function() { /* ... */ });

const Model = mongoose.model('Test', schema);
```

When I call the overridden static, the document-level `save` hooks fire on it, which is clearly wrong — the static is its own method and shouldn't be running document middleware. The same kind of weirdness shows up if I do this with names like `insertMany` or `bulkWrite`.

Mongoose already handles this correctly when the colliding name is a **query** or **aggregate** middleware (e.g. defining `schema.statics.findOne = ...` doesn't auto-wrap it with the `findOne` hook). I'd expect the same behavior for model-level (`bulkWrite`, `insertMany`, `createCollection`) and document-level (`save`, `validate`, `remove`, `updateOne`, `deleteOne`, `init`) middleware: if a user-defined static happens to share a name with one of those, don't auto-apply the corresponding middleware to it.

This currently makes plugins that override built-in methods through statics very awkward to combine with normal hooks.
