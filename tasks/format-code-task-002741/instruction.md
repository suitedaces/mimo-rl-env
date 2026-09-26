Yet another rAF/cAF shim in client.js
Hey, many thanks for the nice project. 

`react-helmet-async` carries requestAnimationFrame shim on board. This is just the 7th rAF shim in our projects bundle. It's [pretty safe][0] to use the API directly in 2018 (yep, we'd also worred about rAF shiming to support old browsers [in 2014][1]).

[0]: https://caniuse.com/#feat=requestanimationframe
[1]: https://stackoverflow.com/questions/21177323/
