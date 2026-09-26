Hello, I'm using the exception mapper to catch exceptions and return them in _json_ format.

The problem is exception code is only mapped into _http header_, but not in the _json response_. 

This is the response I got when my app threw a `ValidationServiceException`:

![Selection_023](https://user-images.githubusercontent.com/496541/83788601-bf6ab200-a695-11ea-89f3-8275a17ae491.png)

This is my config:

```yaml
# Read the documentation: https://symfony.com/doc/master/bundles/FOSRestBundle/index.html
fos_rest:
  param_fetcher_listener:  true
  #  allowed_methods_listener:  true
  #  routing_loader: true
  view:
    view_response_listener:  true
  exception:
    enabled: true
    codes:
      'App\Service\ValidationServiceException': 412
    messages:
      'App\Service\ValidationServiceException': true
    debug: true
    map_exception_codes: true
    flatten_exception_format: 'legacy'
  body_listener: true
  format_listener:
    rules:
      - { path: ^/api/v1, prefer_extension: true, fallback_format: json, priorities: [ json ] }
      # https://github.com/FriendsOfSymfony/FOSRestBundle/issues/631#issuecomment-30321824
      - { path: ^/, prefer_extension: true, fallback_format: ~, priorities: [ html ] }
  disable_csrf_role: ROLE_API
```

Please note I'm using `map_exception_codes` and `flatten_exception_format` options. Also I'm using FosRestBundle v3.0.0.

Could you help me please? I spend all my afternoon with this issue, the sole documentation I found is the one for v2 in Symfony's website.
