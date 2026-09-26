## Actors/UIActors/TileMaps added inside a Timer callback aren't initialized for the current frame

Hi! I've been using Excalibur to build a small game and ran into something
that looks like a bug.

I'm using `Timer`s to spawn things lazily — for example, after a delay,
spawn a pickup, or after the player triggers something, drop in a TileMap
chunk. The pattern looks roughly like this:

```ts
const game = new ex.Engine({ width: 800, height: 600, canvasElementId: 'game' });
const scene = game.currentScene;

scene.add(new ex.Timer(() => {
   const pickup = new ex.Actor(200, 200, 32, 32, ex.Color.Yellow);
   pickup.on('initialize', () => {
      console.log('pickup ready, do setup here');
   });
   game.add(pickup);
}, 500, false));

game.start();
```

The problem: on the frame the timer fires, the new actor visibly shows up,
but its `initialize` event doesn't fire that frame — it only fires on the
*next* frame. Anything I rely on inside `onInitialize` (custom drawings,
sprite setup, child actors, etc.) ends up missing for one frame, so I get
flicker / a wrong-looking first paint of the spawned thing.

I'd expect actors (and UIActors / TileMaps) added to a scene from inside
a timer callback to behave the same way as actors added in `onActivate`
or anywhere else: they should be properly initialized before the scene
draws them.

---

While trying to debug this I also wanted to put a temporary log on
`preupdate` / `postupdate` of one of my TileMaps to see exactly when it
goes through its lifecycle. But it turns out TileMap doesn't expose those
hooks at all — `Actor` and `Scene` let me do `obj.on('preupdate', …)` /
`postupdate` / `predraw` / `postdraw`, but the equivalent on `TileMap`
isn't there. It would be really nice if `TileMap` exposed the same set of
update/draw lifecycle events as the rest of the scene graph, both for
debugging and for attaching custom behavior.

Thanks!
