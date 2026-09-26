Col-end does not support negative values
This is a very small issue, col-end does not support negative values out of the box, but negative values makes a lot of sense there. This happens on **v3.4.3**.

https://play.tailwindcss.com/8L8o0VhDfr

The code is here:

~~~ html
<div class="grid grid-cols-3">
  <div class="-col-end-1">BROKEN</div>
  <div class="col-end-[-1]">WORKS</div>
</div>
~~~

I'm not sure if this is exactly a bug, because it is not explicitly described in the documentation, but it is a broken expectation (I've expected that to work for consistency).
