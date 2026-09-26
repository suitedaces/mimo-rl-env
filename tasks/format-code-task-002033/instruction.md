## Can't override the URLConf used by the blog apphook

I'm integrating `djangocms_blog` in a project and want to customize the
URL patterns the blog apphook serves — I need to tweak a couple of
existing routes and add a few of my own views under the same apphook
mount point. Looking at the apphook registration in
`djangocms_blog/cms_apps.py`, the URL module is hardcoded to
`djangocms_blog.urls` on `BlogApp`, so there doesn't seem to be a
supported way to point the apphook at a different urlconf short of
forking the package or monkey-patching `BlogApp` after import.

Pretty much every other piece of behavior in this package is overridable
through a project-level `BLOG_*` setting, so it would be great if the
apphook's urlconf could be configured the same way. My intended workflow
would be: copy `djangocms_blog/urls.py` into my project as something
like `my_project/blog_urls.py`, adapt it to my needs, and then tell
djangocms_blog to use that module instead of the bundled one.

The default should obviously remain the current `djangocms_blog.urls`
so existing projects that don't set anything keep working as before.

The new setting I'd expect would be something like `BLOG_URLCONF`.
