## `dump_options()` returns invalid JSON when the chart uses `JsCode`

I'm using pyecharts on the backend and just want the chart option object as a JSON string so I can ship it to my own frontend (we render with echarts on the JS side ourselves). `dump_options()` looked like exactly the right thing for this — its name and signature suggest "give me back the option dict as JSON".

For "pure data" charts it works fine — I get a string back and `json.loads` happily parses it. The problem shows up the moment any part of the option uses `JsCode` (typical case for me: a custom `tooltip` formatter that needs a JS function). `dump_options()` returns a string that `json.loads` refuses to parse.

Roughly what I'm doing:

```python
import json
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

bar = (
    Bar()
    .add_xaxis(["A", "B", "C"])
    .add_yaxis("s", [1, 2, 3])
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            formatter=JsCode("function (p) { return p.name + ': ' + p.value; }")
        )
    )
)

raw = bar.dump_options()
print(raw)            # looks JSON-ish, but...
data = json.loads(raw) # ...this blows up
```

Without the `JsCode` line everything is fine and `json.loads(raw)` returns a normal dict. Once `JsCode` is in the picture the returned string isn't valid JSON anymore — the JS function ends up sitting in the output in a way that breaks parsing.

I'd expect `dump_options()` to always return a string that's valid JSON, regardless of whether the option contains `JsCode` values. What the consumer does with those JS snippets afterwards (eval them on the frontend, ignore them, whatever) is on the consumer — but at minimum the result should round-trip through `json.loads` cleanly.

The HTML rendering path (`render()` etc.) doesn't need to change for me; I only care about the explicit `dump_options()` API meant for getting JSON out.
