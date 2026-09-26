Grid.available becomes false negative in SSR environment , and results in opting out of using Grid.
<!--- Provide a general summary of the issue in the Title above -->

### Expected Behavior

 In `SSR` environments like `next-js` , `Grid` should be applicable.

### Actual Behavior

<!--- Tell us what happens instead -->

`Grid` is not applicable because of `Grid.available` evaluating to false

 [Here](https://codesandbox.io/s/lucid-feather-unzm23?file=/pages/index.js) is link for the sandbox code with a `DataChart` , when you refresh the page the chart no more uses grid for layout.

### Steps to Reproduce

Just open the provided Sandbox and refresh the page.

### Your Environment

- Grommet version: 2.22.0
- Browser Name and version:Chrome latest
- Operating System and version (desktop or mobile): Ubuntu 22
