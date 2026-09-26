Unexpected closing tag in html condition comments
**Prettier 1.15.1**
[Playground link](https://prettier.io/playground/#N4Igxg9gdgLgprEAuEAeAhAEQPIGEAqAmgAoCiABABYwC2ANgHwA6Uq19zU55bcAhgBNO3bqhpwYfclD7iAvExAA3AJZwA7gAcIAJxiLykWAhgKQ6lQJiU5AuKrBwAtBauUANORVQVMFXzonAGcwALg5AEYDAHphEVQ-GDo4BlRoxOS4tMp+IRYWUQAjCAEAT3JXazMIgAYagFIDAJUAcygzR2MdRTjRTvgdBhFhkdGx8bGCkYwnJwBtFQAzcgAKFvhyGiCIcgBOAEoAHxWASVJ9gF1UyULkwzg6Ok1BAW8WsxqDR0eg57A3j4GYo6Ow6QEgCqWKqKABsdSadFa7UU-Tg3RA10GCSEGDmCFeiwus168VeSlS0TJJNE6FmC2Waw2Wx2B2OZ0uFJgOPSWPSfFuKVx+KWRKcJLSqMGUzSxTKnGytEYIHcIAgmj80CCyFAfB0Ogg6mIuoQWpQfCUEEsypAhR0fDAAGsJABlP5vZAwHQAVzgKvYdAA6pRfHBfva4M6Tb4VKoYKVkOAglqVd4gmiYMQ7S0aHxkIsAmmVQArIIADwAQnbHS7ZHAADLeOB5gu+kAl0vOt7JACKXog8GbdELIGeOjTOgT-utmh03hgAahlGQAA4aiqZxA0wG7ZoEzPQ2ilE2VTo4ABHL0qU+ZvjZ3NIfND1tpmgqD3e59duC9-tNh8tlUbgXNxkAAJkAu0VERKAWlwCAaBzBMoGgY8QC9NN8H5U1HzTABfXCgA)
```sh
--parser html
```

**Input:**
```html
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title></title>
  </head>

  <body width="100%" align="center">
    <center>                                        
      <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->
      <div></div>
      <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
    </center>
  </body>
</html>
```

**Output:**
```html
SyntaxError: Unexpected closing tag "td". It may happen when the tag has already been closed by another tag. For more info see https://www.w3.org/TR/html5/syntax.html#closing-elements-that-have-implied-end-tags (12:32)
  10 |       <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->
  11 |       <div></div>
> 12 |       <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
     |                                ^
  13 |     </center>
  14 |   </body>
  15 | </html>
```

**Expected behavior:**
```html
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title></title>
  </head>

  <body width="100%" align="center">
    <center>                                        
      <!--[if (gte mso 9)|(IE)]><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tr><td><![endif]-->
      <div></div>
      <!--[if (gte mso 9)|(IE)]></td></tr></table><![endif]-->
    </center>
  </body>
</html>
```
