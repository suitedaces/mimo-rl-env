# Problem Statement

When I'm reviewing our AIP-215 messages, the linter happily lets a field reference a message type that lives outside the API's proto package scope, and nobody catches it. I'd love a rule that flags those foreign message-type references, since they're usually mistakes. Obviously it shouldn't complain about references that remain within the same API package scope, and it should leave the shared/common proto types and AIP component type packages alone. It'd also be nice if versioned subpackages were handled according to the package-scope conventions AIP-215 already expects, so legitimate versioned API subpackages don't trip it up.

# Expected outcomes

- AIP-215 linting reports `core::0215::foreign-type-reference` when a message field references a message type outside the API's proto package scope.
- The rule does not report a problem when the field and referenced message type are within the same API package scope.
- Versioned proto package namespaces are compared using the API-version scope conventions used by AIP-215, so legitimate sibling subpackages within that scope are allowed.
- References to recognized common Google proto packages do not trigger this rule.
- References to AIP component type packages do not trigger this rule.
- Fields that do not reference message types are not reported by this rule.
- The rule has user-facing documentation for `/215/foreign-type-reference`, including the rule purpose, examples of accepted and rejected references, known limitations, and how to disable the rule when necessary.

# Implementation notes

The specific data structures, helper functions, and validation location are up to the implementer. The observable behavior should be integrated with the existing AIP-215 lint rule framework and documentation conventions.
