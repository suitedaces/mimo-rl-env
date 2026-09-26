## Password reset is broken on Django 1.6+

After upgrading my project to Django 1.6, the userena password reset flow no longer works end-to-end. On Django 1.5 the same setup was fine.

Steps to reproduce on a stock userena install:

1. Go to `/password/reset/`, submit a valid email.
2. Receive the password reset email and click the link inside.
3. Try to set a new password.

What actually happens:

- After submitting the email on the reset form, the request errors out instead of landing on the "we've sent you an email" page.
- If I bypass that and click the confirm link from the email directly, the confirm view doesn't match the URL / can't find the user, so I can't actually pick a new password.
- Even when I work around the above, finishing the flow blows up trying to render the "your password has been changed" step.

Everything is plain userena URLs (`include('userena.urls')`) — I haven't overridden the reset views or the email template. The same project works correctly on Django 1.5, so this looks like fallout from changes to `django.contrib.auth`'s password reset views in 1.6.

It would be great to get the password reset flow working on Django >= 1.6 again, while still working on 1.5 (please don't drop 1.5 just to fix this). Ideally without renaming any of the existing `userena_password_reset*` URL names, since I (and presumably others) have `{% url %}` tags and reverse() calls pointing at them from custom templates and code.
