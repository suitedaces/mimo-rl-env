Terms and Privacy checkbox not available with Passwordless mode of Lock
**Issue:**

Currently when using passwordless signup we aren't able to get a checkbox with the `signUpTerms` text and the `mustAcceptTerms` keys set.

This is limited only to the `Auth0LockPasswordless` where as it seems to be working fine when using the database with username-password version of the lock.

We would like to be able to ensure this checkbox/notice display to be in compliance with GDPR and other privacy standards.

- [x] Code snippet or sample project that reproduces the bug

```js
  var clientID = "XXXXXXXXXXXXXXXXXXXX";
  var domain = "freecodecamp.auth0.com";

  var options = {
    languageDictionary: {
      title : "freeCodeCamp.org",
      signUpTerms: "By choosing to continue you confirm that you have read and agreed to..."
    },
    mustAcceptTerms: true,
    theme: {
      ...
    },
    ...
    socialBigButtons : true,
    passwordlessMethod: 'link',
    auth: {
      redirectUrl: 'http://localhost:3000/',
      responseType: 'token id_token',
      params: {
        scope: 'openid profile email'
      }
    },
    allowedConnections: [
      "email", "google-oauth2", "facebook", "github"
    ],
  };

  var lock = new Auth0LockPasswordless(clientID, domain, options);
  lock.show();
```

- [x] Screenshots when appropriate

![image](https://user-images.githubusercontent.com/1884376/41974178-d7c3b1ce-7a34-11e8-8904-6b4496721a0a.png)


- [x] Lock version

```
11.7.2
```

- [x] Browser & OS

```
Not relevant
```

Make sure to include **as much information as possible** for us to understand and reproduce the bug, that way we can fix it as quickly as possible.
