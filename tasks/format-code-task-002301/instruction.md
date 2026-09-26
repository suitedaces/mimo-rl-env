## findRecord hangs forever for missing ids — no way to opt out

After upgrading ember-pouch I noticed that `store.findRecord('post', someId)` no longer rejects when the record doesn't exist. The returned promise just sits in a pending state indefinitely.

Minimal repro in a route:

```js
// app/routes/post.js
export default Ember.Route.extend({
  model(params) {
    return this.store.findRecord('post', params.post_id).catch((err) => {
      console.log('not found:', err);
      this.transitionTo('posts.index');
    });
  }
});
```

If `params.post_id` points at a document that simply isn't in the local PouchDB, the `.catch` never fires, the loading substate never resolves, and the route just hangs. Previously this would reject pretty much immediately and I could redirect the user.

Reading the changelog I see this is intentional — the adapter now waits for replication to eventually deliver the document so that out-of-order belongsTo loads still resolve correctly. I get why that's useful for synced relations, but for plain `findRecord` calls against ids that genuinely don't exist (e.g. a user pasted a bad URL, or I'm doing an existence check) there's no escape hatch — the promise is stuck forever.

Could there be a way to turn this behavior off via `ENV.emberPouch` config so that missing records reject immediately like they used to? Apps that don't rely on the eventual-consistency behavior shouldn't have to live with permanently pending promises, and right now I don't see any documented switch for it.

The flag I'd expect is something like `ENV.emberPouch.eventuallyConsistent = false`.
