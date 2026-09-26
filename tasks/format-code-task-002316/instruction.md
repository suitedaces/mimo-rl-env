Overflowing backtick commands recursively add newlines
## Metadata

* Ruby version: ruby 2.6.3p62 (2019-04-16 revision 67580) [x86_64-linux]
* @prettier/plugin-ruby version: 0.12.2

## Input

```ruby
`this is a very long backtick command that overflows the eighty character line length limit`
```

## Current output

```ruby
`
  this is a very long backtick command that overflows the eighty character line length limit
`
```

which then outputs
```ruby
`
  
  this is a very long backtick command that overflows the eighty character line length limit

`
```

and so on, adding 2 newlines on every format run, eventually leading to something like this

```ruby
`
  
  
  
  
  
  
  this is a very long backtick command that overflows the eighty character line length limit






`
```

## Expected output

```ruby
`
  this is a very long backtick command that overflows the eighty character line length limit
`
```
