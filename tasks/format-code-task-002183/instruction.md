# Better helpers for working with a router's static routes

The libovsdb ops layer that wraps the OVN northbound database has helpers for
logical router static routes, but two common needs are awkward to satisfy today:

1. **Looking up the static routes that belong to a specific router.** The
   existing "find with predicate" helper searches the entire northbound cache
   and returns every matching static route regardless of which router (if any)
   references it. Callers that only care about the routes attached to one
   particular router have to fetch the router and cross-reference UUIDs
   themselves.

2. **Deleting static routes as part of a larger transaction.** The existing
   "delete" helper transacts immediately. There is no way to obtain the
   operations for the deletion so they can be batched together with other
   operations and committed in a single transaction.

Please add two exported helpers to the ops package (the package that already
contains the existing logical-router static-route helpers):

- `GetRouterLogicalRouterStaticRoutesWithPredicate(nbClient, router *nbdb.LogicalRouter, p func(*nbdb.LogicalRouterStaticRoute) bool) ([]*nbdb.LogicalRouterStaticRoute, error)`
  — given a target `*nbdb.LogicalRouter` (identified the same way the other "get
  logical router" helpers identify it) and a static-route predicate, it returns
  the static routes that are **both** referenced by that router **and** satisfy
  the predicate. A static route that satisfies the predicate but is referenced
  by a *different* router (or by no router) must not be returned. If the target
  router does not exist, the call returns an error. When nothing matches it
  returns an empty result and no error.

- `DeleteLogicalRouterStaticRoutesOps(nbClient, ops, routerName string, lrsrs ...*nbdb.LogicalRouterStaticRoute) ([]libovsdb.Operation, error)`
  — an ops-returning variant of the existing static-route delete helper. It
  takes an existing slice of libovsdb operations plus a router name and the
  static routes to delete, and returns the input operations with the additional
  operations appended; it must not transact on its own. Once the returned
  operations are committed, the named routes are removed from the database and
  the router no longer references them. The helper must compose: callers can
  feed it operations produced by an earlier call (e.g. a deletion targeting a
  different router) and commit everything together in one transaction with the
  same end result as committing each step separately.

The existing immediate-transaction delete helper must keep working exactly as
before for its current callers.
