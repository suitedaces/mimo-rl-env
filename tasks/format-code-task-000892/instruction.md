Rule Change: Improve no-html rule's location reporting for HTML tags
### What rule do you want to change?

no-html

### What change do you want to make?

Other

### How do you think the change should be implemented?

Other

### Example code

```markdown
<div id="foo">Some content</div>
```

### What does the rule currently do for this code?

Currently, the rule calculates the end of the reported location for an HTML tag using `start.column + match[0].length + 1`. This typically reports only the tag name itself and an extra character, missing any attributes or trailing spaces within the opening tag. For `<div id="foo">`, it reports `<div `

### What will the rule do after it's changed?

After this change, the rule will report the entire opening HTML tag, including any attributes and spaces, as long as it's on a single line. If the opening tag spans multiple lines, only the first line of the tag will be reported. This aligns with how markdownlint reports similar issues.

- For `<div id="foo">`, it will report the full `<div id="foo">`.
- For `<p\n  data-attribute="value">`, it will report only `<p`.

### Participation

- [x] I am willing to submit a pull request to implement this change.

### Additional comments

_No response_
