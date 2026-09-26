Add `allowFinally` flag to `catch-or-return`
### Description

I would like the option to allow a `finally()` method to follow a `catch()` and still result in a passing `catch-or-return` rule.

This is not a duplicate of #29 and #32 because what I am after is subtly different.  Adding `finally` to `terminationMethod` will allow you to finish a promise with `finally()` _in place_ of a `catch()`, but I would like to allow the use of `finally()` _in addition_ to `catch()`.

e.g. I still want to enforce that Promises are "caught", but allow for a `finally()` callback after it has been caught.  There is currently no way to do this.

### Example

```javascript
// valid when allowFinally: true
showSpinner = true;
service.doSomethingAsync()
    .then(response => {
        console.log('success!', response);
    })
    .catch(err => {
        console.log('error!', err);
    })
    .finally(() => {
        showSpinner = false;
    });

// invalid when allowFinally: true
showSpinner = true;
service.doSomethingAsync()
    .then(response => {
        console.log('success!', response);
    })
    .finally(() => {
        showSpinner = false;
    });

```
