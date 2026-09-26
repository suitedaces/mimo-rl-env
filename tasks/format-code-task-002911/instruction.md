# Add a dark-mode theme store to the frontend

The web app is built with Tailwind configured for class-based dark mode (the `dark`
variant activates when an ancestor element carries the `dark` CSS class). We want a
small, reusable piece of state that the UI can use to drive a light/dark theme toggle.

Add a theme store module to the frontend that the rest of the app can import from
`$lib/store/theme` (i.e. `src/lib/store/theme.ts`). It should expose the following
public surface:

- **`theme`** — a subscribable store holding the current theme, which is always one of
  the strings `'light'` or `'dark'`. Its initial value defaults to `'light'`.
- **`isDark`** — a subscribable, read-only store whose value is the boolean `true` when
  the current theme is `'dark'` and `false` otherwise. It must always stay in sync with
  `theme`.
- **`setTheme(value)`** — sets the current theme. It accepts only `'light'` or `'dark'`.
  Any other value (including `undefined`, `null`, arbitrary strings, or other types) is
  rejected by throwing an `Error`, and the current theme is left unchanged.
- **`toggleTheme()`** — switches the current theme to the other one (`'light'` →
  `'dark'`, `'dark'` → `'light'`).

Whenever the theme changes (and once when the module initializes), the store must keep
two side effects in sync, but only when those browser globals are actually available so
that the module can be imported in a non-browser context without throwing:

- **Document root class** — the root element (`document.documentElement`) must carry the
  `dark` class while the theme is `'dark'`, and must not carry it while the theme is
  `'light'`.
- **Persistence** — after a theme change, the current theme string is written to
  `localStorage` under the key `undb_theme`. On initialization, if `localStorage`
  already holds a valid theme (`'light'` or `'dark'`) under that key, it becomes the
  initial theme; otherwise the default of `'light'` is used. An invalid or missing
  stored value must not throw and falls back to the default.
