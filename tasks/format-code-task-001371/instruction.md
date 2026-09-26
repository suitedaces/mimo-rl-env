## OAuth2 helper not compatible with Django 1.10's `MIDDLEWARE` setting

I'm starting a new Django 1.10 project and trying to integrate the
`oauth2client.contrib.django_util` helper for Google OAuth2 sign-in.

I followed the Django 1.10 release notes and configured my middleware
through the new `MIDDLEWARE` setting in `settings.py`, including
`'django.contrib.sessions.middleware.SessionMiddleware'`. I also added
`oauth2client.contrib.django_util` to `INSTALLED_APPS` as the docs say.

When I run the project, startup fails complaining that session middleware
isn't installed — but it clearly is, just under the new setting name.
If I rename my setting back to the old `MIDDLEWARE_CLASSES`, things start
up fine, but that defeats the point of being on Django 1.10 (the project
template doesn't generate `MIDDLEWARE_CLASSES` anymore, and the old name
is deprecated).

It looks like the helper only knows about the pre-1.10 setting name. Could
the django_util helper be made to work on Django 1.10+ where projects use
`MIDDLEWARE`?
