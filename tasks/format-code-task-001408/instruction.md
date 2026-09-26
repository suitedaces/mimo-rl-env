Color is not applied to Spinner when hpe theme is set
### Expected Behavior

The color set in the color property of the Spinner component should override the theme setting.

### Actual Behavior

It always displays the color which is set in the theme and ignores the color set in the Spinner component.

### URL, screen shot, or Codepen exhibiting the issue

https://codesandbox.io/s/grommet-v2-template-spinner-vw28f?file=/index.js

### Use Case

In a colored button (login/submit/etc.) I want a white spinner and on different backgrounds (white/colored) I want different colored spinner.

### Your Environment

- Grommet version: 2.17.5
- Browser Name and version: any
- Operating System and version (desktop or mobile): windows
