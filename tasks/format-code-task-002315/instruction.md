Error in Ternary Operator
## Metadata

* Ruby version: 2.6.0
* @prettier/plugin-ruby version: 0.12.2

## Input

```ruby
# From ternary:
a ? not(b) : c

# From if:
if a then
  not(b)
else
  c
end
```

## Current output

```ruby
# From ternary:
a ? not b : c

# From if:
a ? not b : c
```

## Expected output

```ruby
# From ternary:
a ? not(b) : c

# From if:
a ? not(b) : c
```
