Generated application adapter tries to import itself
I'm using `0.1.5`

According to the docs:

> `ember generate adapter application` will generate an adapter called ‘ApplicationAdapter’ based off the DS.RESTAdapter by default.

It appears that's not happening and the code that is generated is incorrect.

Run:

```
ember g adapter application
```

output

```
version: 0.1.5
installing
  create app/adapters/application.js
installing
  create tests/unit/adapters/application-test.js
```

The contents of `app/adapters/application.js`:

``` javascript
import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({
});
```

From the docs it seems like it should maybe be:

``` javascript
import DS from 'ember-data';

export default DS.RESTAdapter.extend({
});
```

I notice there is no special handling when generating an adapter named "application" in https://github.com/ember-cli/ember-cli/blob/master/blueprints/adapter/index.js so maybe I'm trying to do something incorrectly.

A bit more info. I landed on this while reading @abuiles book: https://github.com/abuiles/ember-cli-101-errata/issues/124
