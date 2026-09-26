Default file storage is unset by django-upgrade
### Python Version

3.11.3

### Django Version

4.2.4

### Package Version

1.14.0

### Description

Related to the feature added in https://github.com/adamchainz/django-upgrade/pull/321

Today I tried to run django-upgrade on a project where `STATICFILES_STORAGE` was defined in the settings, but not `DEFAULT_FILE_STORAGE`, which caused this change in my settings file:

```diff
- STATICFILES_STORAGE = "my_project.storage.CustomManifestStaticFilesStorage"
+ STORAGES = {
+     "staticfiles": {
+        "BACKEND": "my_project.storage.CustomManifestStaticFilesStorage",
+     },
+ }
```

When I tried to run the tests, I got an error which seems to be caused by the fact that there is no default file storage configured.

<details>
<summary>Stacktrace</summary>

<pre>
Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/core/files/storage/handler.py", line 35, in __getitem__
    return self._storages[alias]
           ~~~~~~~~~~~~~~^^^^^^^
KeyError: 'default'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/core/files/storage/handler.py", line 38, in __getitem__
    params = self.backends[alias]
             ~~~~~~~~~~~~~^^^^^^^
KeyError: 'default'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/bin/pytest", line 8, in <module>
    sys.exit(console_main())
             ^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/_pytest/config/__init__.py", line 189, in console_main
    code = main()
           ^^^^^^

...

  File "/code/projects/onfido/models.py", line 202, in OnfidoCheck
    results_pdf = models.FileField(
                  ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/models/fields/files.py", line 239, in __init__
    self.storage = storage or default_storage
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/utils/functional.py", line 266, in inner
    self._setup()
  File "/usr/local/lib/python3.11/site-packages/django/core/files/storage/__init__.py", line 38, in _setup
    self._wrapped = storages[DEFAULT_STORAGE_ALIAS]
                    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/core/files/storage/handler.py", line 40, in __getitem__
    raise InvalidStorageError(
django.core.files.storage.handler.InvalidStorageError: Could not find config for 'default' in settings.STORAGES.
</pre>

</details>

Since [the setting `DEFAULT_FILE_STORAGE`](https://docs.djangoproject.com/en/4.2/ref/settings/#default-file-storage) defaults to `django.core.files.storage.FileSystemStorage`, should django-upgrade also set this value in the `STORAGES` setting in case the `DEFAULT_FILE_STORAGE` isn't defined?
