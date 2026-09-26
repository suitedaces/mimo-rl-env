# Flatten the message action-row component builders

Building a message action row today is clumsy: to add a button or select menu you
get back a *separate* sub-builder and then have to remember to call a finalising
method on it to actually attach the component to the row. This breaks call chaining
and is easy to get wrong.

Make the message action-row builder able to add components **directly**, in a single
call, returning the row itself so calls can be chained. The standard
`MessageActionRowBuilder` implementation (the one exported from the public builder
implementation module) should grow the following methods.

## Buttons

- `add_interactive_button(style, custom_id, /, *, emoji=UNDEFINED, label=UNDEFINED, is_disabled=False)`
  appends an interactive (non-link) button and returns the action row.
- `add_link_button(url, /, *, emoji=UNDEFINED, label=UNDEFINED, is_disabled=False)`
  appends a link-style button and returns the action row.

`emoji` accepts a custom-emoji object/ID or a unicode emoji/string; `label` is the
button's text; `is_disabled` marks it disabled.

## Select menus

- `add_select_menu(type_, custom_id, /, *, placeholder=UNDEFINED, min_values=0, max_values=1, is_disabled=False)`
  appends a select menu of the given type and returns the action row. This is the
  method for the user / role / mentionable select-menu types; channel and text
  select menus have their own dedicated methods (below). Passing a value that is not
  a valid select-menu component type must raise `ValueError`.
- `add_channel_menu(custom_id, /, *, channel_types=(), placeholder=UNDEFINED, min_values=0, max_values=1, is_disabled=False)`
  appends a channel select menu and returns the action row. `channel_types`
  restricts which channel types may be picked (empty means no restriction).
- `add_text_menu(custom_id, /, *, placeholder=UNDEFINED, min_values=0, max_values=1, is_disabled=False)`
  appends a text select menu and, because such a menu needs its options filled in,
  returns the *text-select-menu builder* (not the row).

The returned text-select-menu builder must expose:

- a `parent` property that returns the action row the menu was added to, so callers
  can hop back and continue building the row; and
- `add_option(label, value, /, *, description=UNDEFINED, emoji=UNDEFINED, is_default=False)`
  which appends an option to that menu and returns the menu builder (so options can
  be chained). `emoji` follows the same custom/unicode handling as buttons.

The menu must already be attached to the row as soon as `add_text_menu` returns
(before any options are added).

## Single component type per row

An action row may only hold one kind of component. Adding a component whose type
differs from what the row already contains must raise `ValueError`.

## Serialized output

When the action row is built, each added component must appear inside the row's
`"components"` list serialized to the Discord payload shape:

- Buttons → `{"type": 2, "style": <style>, "disabled": <is_disabled>, ...}`. Link
  buttons carry `"url"`; interactive buttons carry `"custom_id"`. `"label"` is
  present only when a label was given. When an emoji was given, an `"emoji"` object
  is present: `{"id": "<id>"}` for a custom emoji (object or integer ID) or
  `{"name": "<emoji>"}` for a unicode/string emoji.
- Select menus → `{"type": <type>, "custom_id": <custom_id>, "min_values": <min>,
  "max_values": <max>, "disabled": <is_disabled>}`, with `"placeholder"` present only
  when one was given. The type values are `5` (user), `6` (role), `7` (mentionable),
  `8` (channel) and `3` (text). Channel menus additionally carry `"channel_types"`.
  Text menus additionally carry an `"options"` list, each option serialized as
  `{"label": <label>, "value": <value>, "default": <is_default>}` with
  `"description"` and `"emoji"` present only when supplied (emoji using the same
  shape as buttons).
