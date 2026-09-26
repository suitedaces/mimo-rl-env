## Feature request: a way to query which API actions are available

I'm building a third-party tool on top of AnkiConnect (similar to how Yomichan integrates with it) and I'd like to do **feature detection** at runtime — i.e. before I call some action, figure out whether the user's installed AnkiConnect actually supports it.

The use case is pretty standard: AnkiConnect grows new actions over time, and not every user is on the same version. If my tool wants to use a newer action when it's available and fall back to something else when it isn't, I need a way to ask the server "do you support action X?".

Right now the only way I've found to do this is to just go ahead and send the request, and then look at the response — if I get back

```json
{"result": null, "error": "unsupported action"}
```

then I know it's not supported. This works, but it's pretty awkward:

- I have to actually invoke the action (with plausible-looking params) just to probe for it, which feels wrong for actions that have side effects.
- If I want to probe several candidate actions to pick the best one available, I have to fire one request per action and parse the error string of each. There's no batch way to do it.
- "Parse the error message of a failed call" isn't a great contract to build on — it would be nicer to have a first-class way to ask the question.

Could AnkiConnect expose a dedicated action for this? Something I can call to either get the list of all actions this instance supports, or to pass in a list of action names I care about and have the server tell me which subset of those it actually has. That way third-party clients can do clean capability checks without abusing the error path.

Happy to consume whatever shape of response makes sense on your side — I mainly just need the information to be queryable through the normal request/response interface. The new action I'd expect is something like `apiReflect`, taking `scopes` and `actions` params and returning a result keyed by those same scope names (e.g. `{"scopes": [...], "actions": [...]}`).
