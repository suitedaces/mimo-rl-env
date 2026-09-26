## Dummy-coding categorical values in a Timeline

A bunch of the extractors I'm using produce categorical / string-valued features — e.g. detected object labels, face expression categories, speech tokens, etc. When I build a `Timeline` from these and call `to_df()`, the resulting DataFrame has columns full of strings.

That's fine for inspection, but the moment I want to actually do something quantitative with it (correlations, regressions, feeding it into sklearn, etc.) I have to go and one-hot / dummy-code those columns myself outside of pliers, which is annoying and easy to get wrong when the same categorical variable appears at many different onsets across the Timeline.

It would be really useful if `Timeline` itself could give me back a version where categorical variables are expanded into binary indicator variables, so that the output of `to_df()` is directly usable in numeric pipelines. Numeric columns should be left alone — I only want the string-typed ones expanded by default — though being able to force expansion of all variables would also be handy for some use cases.

I'm imagining the API as something like `tl.dummy_code(...)` returning a new Timeline, with a flag (e.g. `string_only`) to toggle whether numeric columns are also expanded.
