Fix false positives for shared-line comments in value-list-comma-newline-after
<!-- Please answer the following questions. Issues that don't use this template will be closed. -->

> Describe the issue. Is it a bug or a feature request (new rule, new option, etc.)?
Improve rule `value-list-comma-newline-after`.
At the moment I can't put comments after commas, like:

````css
a { background-size: 0, // comment fails here...
      0; }
````

> Which rule, if any, is this issue related to?

`value-list-comma-newline-after`

> What CSS is needed to reproduce this issue?

```css
a { background-size: 0, // comment fails here...
      0; }
```

> What stylelint configuration is needed to reproduce this issue?

```json
{
  "rules": {
    "value-list-comma-newline-after": "always-multi-line"
  }
}
```

> Which version of stylelint are you using?

`8.1.1`

> How are you running stylelint: CLI, PostCSS plugin, Node API?

stylelint-webpack-plugin

> Does your issue relate to non-standard syntax (e.g. SCSS, nesting, etc.)?

Nope

> What did you expect to happen?

No warnings to be flagged

> What actually happened (e.g. what warnings or errors you are getting)?

"The following warnings were flagged:"

```shell
ERROR in 
src/styles/_fonts.scss
  8:37  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
  9:93  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 10:76  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 11:74  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 12:77  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 13:88  ✖  Expected empty line before comment                comment-empty-line-before     
 23:38  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 24:89  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 25:72  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 26:70  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 27:73  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 28:84  ✖  Expected empty line before comment                comment-empty-line-before     
 38:34  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 39:89  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 40:72  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 41:70  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 42:73  ✖  Expected newline after "," in a multi-line list   value-list-comma-newline-after
 43:84  ✖  Expected empty line before comment                comment-empty-line-before
```
<!--
Before posting, please check that your issue:
1. Hasn't already been resolved in:
  - the next release (https://github.com/stylelint/stylelint/blob/master/CHANGELOG.md)
  - an upcoming major milestone (https://github.com/stylelint/stylelint/milestones)
2. Hasn't already been discussed (https://github.com/stylelint/stylelint/search)
-->

<!--
Here are the best ways to help resolve your issue:
1. Figure out what needs to be done, propose it, and then write the code and submit a PR.
2. If your issue is a bug, consider at least submitting a PR with failing tests.

Note: GitHub issues are for stylelint bugs and enhancements, if you're looking for help or support with stylelint then stackoverflow is our preferred question and answer forum - http://stackoverflow.com/questions/tagged/stylelint
-->
