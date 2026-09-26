Less-than or greater-than sign in text
It appears that you can't currently use `<` or `>` characters in text.

For example, this markdown:

```markdown
# Hello, MDX
  
I <3 Markdown and JSX
```

Produces this JSX:

```jsx
export default ({components}) => <MDXTag name="wrapper"><MDXTag name="h1" components={components}>Hello, MDX</MDXTag>
<MDXTag name="p" components={components}> I <3 Markdown and JSX</MDXTag></MDXTag>
```

Which fails to compile in babel.

MDXC compiles this the following way:

```jsx
export default function({ factories={} }) {
  const {
    h1 = createFactory('h1'),
    p = createFactory('p'),
    wrapper = createFactory('div'),
  } = factories

  return wrapper({},
    h1({"id": "Hello-MDX"},
      "Hello, MDX",
    ),
    p({},
      "I <3 Markdown and JSX",
    )
  )
}
```
