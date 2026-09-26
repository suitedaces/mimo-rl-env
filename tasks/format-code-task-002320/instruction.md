Improve mutliline template strings
This may have been discussed in a previous issue about template strings but I couldn't remember that I've seen such a discussion and didn't find a corresponding issue.

I am using multiline template strings quite often and they often create bad looking code with Prettier. I know that's hard to format around template strings because you can't change the meaning of the code.

Currently, I have 2 use cases where I think we can improve the output of prettier.

## Template string in constructor

Input / Desired:
```js
throw new Error(formatErrorMessage`
    This a really bad error.
    
    Which has more than one line.
`)
```

Output:
```js
throw new Error(
  formatErrorMessage`
    This a really bad error.
    
    Which has more than one line.
`
);
```

## Template string in chained function call

Input / Desired:
```js
func1(func2(func3(formatErrorMessage`
    This a really bad error.
    
    Which has more than one line.
`)))
```

Output:
```js
func1(
  func2(
    func3(formatErrorMessage`
    This a really bad error.
    
    Which has more than one line.
`)
  )
);
```

## Possible Solution

Maybe we could handle multiline template strings like single line strings (with a zero length).
This may produce some unexpected output at some other places so we would have to test different scenarios.

Hopefully, this wasn't discussed before and we can improve the output.
