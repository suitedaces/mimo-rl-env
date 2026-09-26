# Publish authentication & LMS connection details in the frontend context

Every Richie page embeds a JSON "frontend context" (rendered into the page as
`window.__richie_frontend_context__`) that the JavaScript application reads at boot time.
Today it only carries a handful of generic values (csrf token, environment, release,
sentry dsn). The frontend now needs to know **where and how to talk to the authentication
service and to the LMS backends**, so this configuration has to be exposed through that same
context.

Please extend the context that feeds the templates so that:

## 1. A new `AUTHENTICATION_DELEGATION` setting

Introduce a project setting named `AUTHENTICATION_DELEGATION`. It is a mapping with the
following keys:

- `BASE_URL`: the base URL of the authentication service (a string).
- `BACKEND`: an identifier of the authentication backend to use (a string).
- `PROFILE_URLS`: an ordered list of `{"label": ..., "href": ...}` entries describing links to
  the user's profile pages on the authentication service. Inside `href`, the placeholder
  `{base_url}` must be substituted with `BASE_URL`; any other text (including other
  placeholders) is left untouched.

The default configuration shipped with the project must define this setting so that pages keep
rendering as before.

## 2. Authentication & LMS info inside the frontend context

The object found under the `context` key of the frontend-context JSON must gain two new entries:

- `authentication`: an object `{"endpoint": <BASE_URL>, "backend": <BACKEND>}` taken from
  `AUTHENTICATION_DELEGATION`.
- `lms_backends`: a list built from the `LMS_BACKENDS` setting — **one object per configured
  backend, in order**. Each object has exactly these keys:
  - `endpoint`: the backend's `BASE_URL`,
  - `backend`: the backend's `BACKEND`,
  - `course_regexp`: the backend's `JS_COURSE_REGEX`,
  - `selector_regexp`: the backend's `JS_SELECTOR_REGEX`.

  When no LMS backend is configured, this must be an empty list.

## 3. Profile URLs available to the templates

Expose a new top-level template-context variable `AUTHENTICATION` containing a single key
`PROFILE_URLS`. Its value is a **JSON-encoded string** of a list of objects, one per entry of
`AUTHENTICATION_DELEGATION["PROFILE_URLS"]`, preserving order, where each object has:

- `label`: the configured label, as a string,
- `action`: the configured `href` with `{base_url}` resolved against `AUTHENTICATION_DELEGATION["BASE_URL"]`.

The existing generic values already present in the frontend context, as well as the other
template-context information, must remain unchanged.
