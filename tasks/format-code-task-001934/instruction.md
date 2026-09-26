Not a bug, but definitely a (small) missed optimization. Without default args, the redundancy does not appear.

**Uglify version (`uglifyjs -V`)**
uglify-js 3.13.8

**JavaScript input**
```js
function f({base='',r}={}) { return base + r }
```

**The `uglifyjs` CLI command executed**
`uglifyjs testcase.js --mangle reserved=['base','r'] -c`

**JavaScript output**
```js
function f({base:base="",r}={}){return base+r}
```
