## README map-reduce example doesn't run

Just trying communist out for the first time — looks great for what I want to do (crunch some numbers across a few workers). I copy-pasted the map-reduce example straight from the README:

```js
var worker = communist(4);
//pass it the number of map workers
worker.data([1,2,3]);
worker.map(function(x){return x*x;});
worker.reduce(function(a,b){return a+b;});
worker.data([4,5,6]);
worker.fetch().then(function(a){console.log(a)});
// README says this should print 91
worker.data([6,7,8]).fetch().then(function(a){console.log(a)});
// and this should print 240
worker.close().then(function(a){console.log(a)});
// and this should print 389
```

When I run this, it blows up on the `worker.fetch()` line — the object I get back from `communist(4)` doesn't seem to have a `fetch` (or a `close`). I only get `.data`, `.map`, `.reduce` on it. So none of the lines after the initial three setup calls actually work.

Is the README out of date, or is `communist(N)` supposed to give back the object the README describes (the one with `data` / `map` / `reduce` / `fetch` / `close`, where you can keep feeding it data and ask for results whenever)? That's the workflow I'm after — incrementally pushing chunks in, occasionally fetching the running result, and closing manually when I'm done.
