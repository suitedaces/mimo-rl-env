## Catch missing Parler-related settings at application load time

When integrating Shuup into a Django project, it's quite easy to set up the obvious bits (INSTALLED_APPS, the database, etc.) but forget about the Parler-related settings that Shuup actually depends on (things like `PARLER_DEFAULT_LANGUAGE_CODE` and `PARLER_LANGUAGES`). Nothing in Shuup itself flags their absence early on, so the application starts importing fine and only blows up later, somewhere deep inside translation/model handling, with a message that has nothing to do with "you forgot to configure Parler".

This is a pretty rough first-time experience: newcomers end up chasing the failure through their own models or data, or assuming there's a bug in Shuup, when in reality they're just missing a couple of settings in their `settings.py`.

It would be much nicer if Shuup refused to come up at all when the Parler settings it relies on are not configured, and told you upfront which setting is missing. That way the misconfiguration is caught at application load time with a clear, actionable error, rather than as some opaque downstream failure once the application is already running.

I'd expect the failure to be signalled via a dedicated exception class exposed from `shuup.core`, something along the lines of `MissingSettingException`.
