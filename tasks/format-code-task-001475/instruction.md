createFeed with key and opts.key - opts.key overwrites key
Just got pretty confused by this happening:

```js
var opts = {
  key: 'f4d436e799f5466fa98eee04d52354e155bce62ba584393c2907a38b02d96a19',
  etc..
}

var key = Buffer(opts.key, 'hex')
var feed = core.createFeed(key, opts)
```

This leads to an error because `opts.key` is the one passed to `feed()` but it is only [set if opts.key](https://github.com/mafintosh/hypercore/blob/master/index.js#L48) is null.

```
Error: key should be a 32 byte buffer
    at new Feed (/Users/joe/node_modules/dat-node/node_modules/hypercore/lib/feed.js:29:49)
    at Feed (/Users/joe/node_modules/dat-node/node_modules/hypercore/lib/feed.js:21:39)
    at Hypercore.createFeed (/Users/joe/node_modules/dat-node/node_modules/hypercore/index.js:56:11)
```

I didn't realize `opts.key` was being passed through. We can either document this or check `opts.key` for validity. I can PR something for this!
