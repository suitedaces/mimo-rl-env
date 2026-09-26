getByRole(role, { current: true })
<!--

Vote on feature requests by adding a 👍. This helps maintainers prioritize what
to work on.

* Please fill out this template with all the relevant information so we can
  understand what's going on and fix the issue. We appreciate bugs filed and PRs
  submitted!

* Please make sure that you are familiar with and follow the Code of Conduct for
  this project (found in the CODE_OF_CONDUCT.md file).

It'd be great if after the discussion you're the one who submits the PR that
implements this feature. If you've never done that before, that's great! Check
this free short video tutorial to learn how: https://kcd.im/pull-request


If this is an issue with the documentation, please file an issue in the docs repo:
https://github.com/testing-library/testing-library-docs
-->

### Describe the feature you'd like:

<!--
A clear and concise description of what you want to happen. Add any considered
drawbacks.
-->
The [getByRole query](https://testing-library.com/docs/dom-testing-library/api-queries#byrole) is very versatile and helpful in helping us put accessibility at the forefront of our testing. It currently includes options like `selected`, `checked` to select based on state. This is great but it seem to be missing out on one of such states that is usually defined by users to determine active/current section: [aria-current](https://www.aditus.io/aria/aria-current/). It will be great if we can pass that option that checks for this aria attribute
### Suggested implementation:

<!-- Helpful but optional 😀 -->
Since `aria-current` may be used in different ways e.g `aria-current="page"`, `aria-current="location"`, `aria-current="step"` we may consider making the option take a string like:
```js
getByRole("button", { current: "page" })
```
but so far in my presumed usage it seem like this can be sufficient as:
```js
getByRole("button", { current: true })
```
checking only the existence of the `aria-current` attribute as it's unlikely more than one type is being tested at a time.
