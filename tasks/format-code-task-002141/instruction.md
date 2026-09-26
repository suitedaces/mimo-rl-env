## Consolidate the `toggle` and `toggle-control` Stimulus controllers

We currently have two Stimulus controllers in `app/webpacker/controllers/` that do morally the same thing — they read the state of an input and use it to flip the state of some other element(s):

- `toggle_controller.js` — shows/hides `content` targets based on a `data-toggle-show` attribute on the triggering input.
- `toggle_control_controller.js` — enables/disables `control` targets depending on whether an input has a value.

There is already a `//todo:` line sitting in `toggle_control_controller.js` asking whether a new method on that controller could replace `ToggleController` entirely. It'd be nice to actually do this clean-up so we aren't carrying two controllers that overlap in responsibility.

The only place I can see `ToggleController` still in use is the checkout details view (`app/views/checkout/_details.html.haml`), where it's wired up alongside the `shippingmethod` controller on the shipping section:

```
%div.checkout-substep{ "data-controller": "toggle shippingmethod" }
```

It's used to show/hide the "ship address" sub-form and the "save shipping address" checkbox when a shipping method that requires a separate address is selected. That UX should keep working exactly as it does today after the refactor.

So in short: fold the show/hide behaviour into the existing toggle-control controller, migrate the checkout view to use the consolidated controller, and drop `toggle_controller.js`.
