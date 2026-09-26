single-line-per-selector is seeing inline comments as selectors
<!--

Please include as much information as possible about your issue/request.

Make sure you've read through our [contribution guidelines](https://github.com/sasstools/sass-lint/blob/develop/CONTRIBUTING.md#submitting-issues) first.

If you would like to propose a feature please ignore some of the headings below but include as much information as you can and if possible any relevant test case code samples.
-->

**What version of Sass Lint are you using?**
**gulp-sass-lint 1.2.0**, which I believe is using **sass-lint 1.8.0** 

**Please include any relevant parts of your configuration:**
`single-line-per-selector` is enabled.

**What did you do? Please include the actual source code causing the issue.**
I'm adding inline comments to the end of selectors/properties. See issue below:

```
button,
html input[type='button'], // 6
input[type='reset'],
input[type='submit'] {
    -webkit-appearance: button; // 7
    cursor: pointer; // 8
}
```

**What did you expect to happen?**
I expect the linter to run over this block of code and conclude that there is only one CSS selector per line (because there is).

**What actually happened? Please include any error messages given to you by Sass Lint.**
It's hating on one particular inline comment, this line:

```
html input[type='button'], // 6
```

Here's the error message:
`42:27  warning  Selectors must be placed on new lines  single-line-per-selector`

**What I would like to see changed:**
Comments, whether css comments `/* */` or sass comments `//` shouldn't be noticed by the linter at all, or at the very least not in the way its currently believing that the comment is a second selector.
