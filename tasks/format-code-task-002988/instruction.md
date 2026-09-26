BannerPlugin: Accept a Function in addition to String/Object
<!-- Please don't delete this template or we'll close your issue -->

## Feature request

<!-- Issues which contain questions or support requests will be closed. -->
<!-- Before creating an issue please make sure you are using the latest version of webpack. -->
<!-- Check if this feature need to be implemented in a plugin or loader instead -->
<!-- If yes: file the issue on the plugin/loader repo -->
<!-- Features related to the development server should be filed on this repo instead -->

**What is the expected behavior?**

I'd like to see the BannerPlugin accept a function in addition to a string or an options object, similar to [`config.output.filename`](https://webpack.js.org/configuration/output/#output-filename). The function would have access to a `chunk` variable or anything else necessary for an actual reference to `'[hash]'`, `'[chunkhash]'`, `'[name]'`, `'[filebase]'`, `'[query]'`, and `'[file]'`.

**What is the motivation or use case for adding/changing the behavior?**

With references to information about each chunk being processed, the banner can be programmatically customized; for example:

```js
// webpack.config.hypothetical.js

import {BannerPlugin} from 'webpack';

// other variables declared in outer scope (libName, etc.)
const banner = new BannerPlugin(({ name }) => ({

  banner: `${libName} (${description})

${name.includes('something') ? doSomething() : elseDoSomethingElse()} v${version}

Copyright (c) 2018-present, ${author}

This source code is licensed under the ${license} license found in this library's GitHub repository (${licenseUrl}).`,

  entryOnly: true,

  // ... etc.
}));
```

**How should this be implemented in your opinion?**

I took a look at the BannerPlugin codebase and it looks doable, but there were some parts where I'm not sure what's going on. Sorry I can't be more specific at this time.

**Are you willing to work on this yourself?**

Yes, but...
- I won't have time to work on it for at least 3-4 weeks
- I'm not yet familiar with Webpack's codebase
