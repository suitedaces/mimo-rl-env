# Add lifecycle event handlers to `toga.Window`

Right now a `Window` only lets you respond to one lifecycle event, `on_close`.
Applications frequently need to react to a window changing its focus or
visibility — for example, pausing background work when a window is hidden, or
refreshing data when it comes back to the foreground.

Add four new optional event handlers to `toga.Window`:

- `on_gain_focus` — the window became the application's current (focused) window.
- `on_lose_focus` — the window stopped being the application's current window.
- `on_show` — the window became visible.
- `on_hide` — the window stopped being visible.

## Expected behavior

- Each handler must be available **both** as a keyword argument to the `Window`
  constructor **and** as a readable/writable property, in exactly the same way
  the existing `on_close` handler works. Assigning a new callable to the
  property replaces the handler.
- When a handler has not been provided, reading the property must still return a
  callable (a no-op), consistent with how an unset `on_close` behaves.
- Whenever a handler fires, it is invoked with the window instance it belongs
  to.

The handlers fire in response to the following observable state changes:

- **Visibility.** When a window transitions from not-visible to visible, its
  `on_show` handler fires; when it transitions from visible to not-visible, its
  `on_hide` handler fires. This applies whether visibility is changed through
  `show()`/`hide()` or through the `visible` property. A request that does not
  actually change the visibility (e.g. showing an already-visible window) must
  not fire either handler.
- **Minimize / restore.** Moving a visible window into the minimized state fires
  its `on_hide` handler; restoring it from the minimized state back to a visible
  state fires its `on_show` handler. Switching between other window states does
  not fire these handlers, and a state request that leaves the state unchanged
  fires nothing.
- **Focus.** When the application's current window changes from one window to a
  different window, the window that was current has its `on_lose_focus` handler
  fired, and the window that becomes current has its `on_gain_focus` handler
  fired. Setting the current window to the window that is already current fires
  neither handler.

Adding these handlers should not disturb the existing `on_close` behavior.
