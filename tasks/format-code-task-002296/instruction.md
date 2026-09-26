Problem Statement: When I pull matchbox into my Go project, my dependency tooling complains because it sees both `github.com/Sirupsen/logrus` and `github.com/sirupsen/logrus` as different packages. I’m already using the lowercase logrus path everywhere else, so matchbox is the odd one out and it can break builds on my setup. Can you make matchbox use the canonical lowercase logrus dependency so it resolves cleanly with the rest of the ecosystem?

Expected outcomes:
- matchbox’s Go sources and dependency metadata should consistently use `github.com/sirupsen/logrus`, so the project no longer exposes mixed-case logrus paths to downstream builds.
- The repository’s dependency manifest and lock metadata should resolve that lowercase logrus dependency at the intended `v1.3.0` release.
- A downstream project that already depends on `github.com/sirupsen/logrus` should be able to build matchbox-related packages without dependency-path conflicts caused by the old mixed-case import path.
- Existing repository tests should continue to pass with the canonical lowercase dependency path in place.

Implementation notes:
- The exact regeneration or update steps used to keep dependency metadata consistent are up to the implementation.
- Any internal dependency-management housekeeping beyond the observable dependency-path/version outcome is left to the implementer.
- Keep the change focused on the externally visible dependency-resolution result rather than on any particular internal organization.
