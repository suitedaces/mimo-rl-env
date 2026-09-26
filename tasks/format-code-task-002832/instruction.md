## Time field has no way to customize its display format

On my dashboard I have a model with a `time` attribute (think "store opening time" — just an hour of day, no date). Administrate renders it like `09:00AM`, but I want it shown in 24-hour form (e.g. `09:00`).

For `date` and `datetime` fields I can already do this from the dashboard:

```ruby
class StoreDashboard < Administrate::BaseDashboard
  ATTRIBUTE_TYPES = {
    opens_on:  Field::Date.with_options(format: "%Y-%m-%d"),
    opens_at:  Field::DateTime.with_options(format: "%Y-%m-%d %H:%M"),
    opens_time: Field::Time, # <-- no format option available
  }
end
```

But `Field::Time` doesn't accept a format option at all — looking at the rendered output, the time partials always print the attribute with the same hard-coded 12-hour `HH:MMam/pm` style regardless of what I pass in `with_options`.

It would be great if `Field::Time` supported the same `format:` option that `Field::Date` and `Field::DateTime` already support, so users can pick their own time representation.

One thing to keep in mind: existing apps relying on the current default output shouldn't break — when no format is provided, the field should keep rendering the same way it does today.

I'd expect the field to expose something like a `time` helper method that the partials can call to get the formatted string.
