Used var declaration is removed with default reduce_vars=true
**Bug report or feature request?**
bug

**Uglify version (`uglifyjs -V`)**
uglify-js 3.6.0

**JavaScript input**
UglifyJs.minify(\`
function xxx(module) {
  function fun() {
    console.log(MODE.BlockStatement === 'a');
  }
  var MODE = {
    BlockStatement: 'BlockStatement',
  };
  module.exports = fun;
}
\`)

**The `uglifyjs` CLI command executed or `minify()` options used.**
use deafult options

**JavaScript output or error produced.**
function xxx(o){o.exports=function(){console.log("a"===c.BlockStatement)}}

PS: `var MODE = {
    BlockStatement: 'BlockStatement',
  };` was removed unexpected and result in runtime error

while the UglifyJs output is ok with the options
`{
  compress: {
    reduce_vars: false
  }
}
`


`function xxx(t){function o(){console.log("a"===e.BlockStatement)}var e={BlockStatement:"BlockStatement"};t.exports=o}`
