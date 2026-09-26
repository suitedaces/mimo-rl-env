## Console errors when scrolling through certain iRegs interpretations pages

I was browsing the interpretations pages on the regulations site and noticed that the dev tools console fills up with errors as soon as I start scrolling. The wayfinder component (the little floating thing at the top that shows the current section/paragraph) seems to be involved.

### Steps to reproduce

1. Visit `https://www.consumerfinance.gov/policy-compliance/rulemaking/regulations/1002/Interp-9/` (or run it locally).
2. Open the dev tools console.
3. Scroll down through the page.

### What I see

The console starts spitting out errors like:

```
Uncaught TypeError: Cannot read property 'split' of undefined
```

They keep firing as I scroll past the early paragraphs on the page. Other interpretations pages I've poked at seem fine, but this one (and I suspect a few others) reliably blows up.

### What I expect

Scrolling through any interpretations page should not throw errors in the console. The wayfinder should keep working — or at minimum fail gracefully — even on pages whose content has unusual paragraph structure.
