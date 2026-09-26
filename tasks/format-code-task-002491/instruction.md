URL with unicode characters will not load in MS Edge
## Description

When you have a route path containing a unicode character, it is recommended to use `encodeURI` so reach router supports it correctly. This works well in all browsers but it doesn't work in MS Edge.

Example:
```javascript
<Router>
  <App path="/">
      <Home path="/" />
      <Unicode path={encodeURI("påge")} />
  </App>
</Router>
```

After some investigation, it seems that in MS Edge, the `window.location.pathname` is not url encoded, but other browsers encode it.
This results in not found route when a url contains a special character.

I have opened a pull request to suggest a fix, see https://github.com/reach/router/pull/344

### Steps to reproduce

* Open the following code sandbox in Edge. https://codesandbox.io/s/reach-router-starter-v1-8ooex
* In the UI, click on `Unicode page` link

In Chrome, you'll see the page title `Page with unicode in url works !`, but in MS Edge you don't


### Related Issues

I've discovered this bug by digging into a gatsby issue. See https://github.com/gatsbyjs/gatsby/issues/17556
