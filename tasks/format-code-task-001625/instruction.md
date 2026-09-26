## Can't reuse the configured i18next instance from `i18n.js` in tests

I'm trying to add some Jest tests for components in this project. A lot of our components render translated strings via `react-i18next`, so in the tests I need access to the i18next instance that's already configured in `i18n.js` (with all the `langs/*.json` resources, fallback language, etc.).

The problem is that `i18n.js` doesn't export anything — it just imports `i18next`, calls `i18next.use(initReactI18next).init({ ..., resources })` as a side effect, and that's it. So from a test file I can't actually get a handle on the configured instance, nor on the `resources` map. My options right now are:

- import `i18n.js` purely for its side effect and hope the singleton inside `i18next` is the one my component is using — fragile and hard to assert against in tests, or
- duplicate the whole resource bundle / init call inside the test setup — defeats the point of having `i18n.js` in the first place.

It would be really helpful if `i18n.js` actually exposed the things it sets up so test files can import and use them directly.

While we're at it, it'd also be nice to have Jest's TypeScript types available as a devDependency so editors / type checking don't choke on `describe` / `it` / `expect` in test files.
