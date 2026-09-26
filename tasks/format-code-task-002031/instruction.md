### Connection-based aggregate returns inflated / wrong values when target nodes appear via multiple paths

When I use the new connection-based aggregation API to compute things like `sum`, `average`, `min`, `max` on a related entity's attribute, the numbers come out larger than they should be. It looks like the same target node is being counted more than once.

**Schema (simplified)**

```graphql
type User @node {
  name: String!
  liked: [Post!]! @relationship(type: "LIKED", direction: OUT)
}

type Post @node {
  title: String!
  likes: Int!
}
```

**Query**

```graphql
{
  users {
    likedConnection {
      aggregate {
        node {
          likes {
            sum
            average
            max
          }
        }
      }
    }
  }
}
```

**What I see**

The `sum` and `average` reported by the connection aggregate don't match what I get if I just open Neo4j Browser and run something like

```cypher
MATCH (u:User)-[:LIKED]->(p:Post)
RETURN sum(p.likes), avg(p.likes), max(p.likes)
```

restricted to the same users. The connection-based aggregate consistently overshoots — clearly some posts are being included multiple times in the aggregation (e.g. when several users in the result set liked the same post).

I see the same kind of wrongness on string fields too — `longest` / `shortest` from a connection aggregate sometimes picks a value that only makes sense if duplicates are being kept.

**What I expected**

The connection aggregate should aggregate over the *distinct* set of target nodes — each Post should contribute to `sum`/`average`/`max`/etc. once, regardless of how many edges in the traversal happen to land on it. That matches how I'd describe the query in English ("the sum of likes across the liked posts") and how a hand-written Cypher aggregation behaves.

This makes the new `connection { aggregate { ... } }` API basically unusable for numeric or string aggregations on a many-to-many style relationship, because the answers are just wrong.
