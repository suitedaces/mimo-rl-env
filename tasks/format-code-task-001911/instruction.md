### Return `peg::ast<>` by value from the parsing helpers

Right now the GraphQL parsing entry points all hand back a `std::unique_ptr`:

```cpp
std::unique_ptr<peg::ast<std::string>>             parseString(std::string&& input);
std::unique_ptr<peg::ast<std::unique_ptr<file_input<>>>> parseFile(const char* filename);
std::unique_ptr<peg::ast<const char*>>             operator "" _graphql(const char*, size_t);
```

…and `service::SubscriptionParams::query` is also a `std::unique_ptr<peg::ast<std::string>>`.

This is awkward at every call site:

```cpp
auto ast = R"({ appointments { edges { node { id } } } })"_graphql;
// have to write *ast->root everywhere just to hand the AST to the service
auto result = _service->resolve(state, *ast->root, "", std::move(variables)).get();
```

```cpp
if (!ast)            // null check on the pointer
    throw std::logic_error("...");

for (const auto& child : ast->root->children) { ... }
```

The `unique_ptr` here doesn't really buy anything — `peg::ast<>` is just a small struct holding the input buffer plus a `unique_ptr<ast_node> root`. Forcing every caller through one extra heap allocation and an extra layer of pointer indirection (`ast->root` vs `ast.root`, `*ast->root` vs `*ast.root`) makes the API more verbose than it needs to be, and it makes it harder to move/return parsed ASTs around naturally (e.g. building a `SubscriptionParams` from a freshly parsed query).

It would be much nicer if `peg::ast<>` were a regular movable value type and the parsing helpers (and the user-defined literal) just returned it by value:

```cpp
auto ast = R"(...)"_graphql;
if (!ast.root) { /* parse failed */ }
auto result = _service->resolve(state, *ast.root, "...", std::move(variables)).get();
```

…and likewise `SubscriptionParams::query` could just hold a `peg::ast<std::string>` directly, with callers `std::move`-ing one in.

I realise this is a breaking change to the public API surface (every caller of `parseString` / `parseFile` / `_graphql`, plus anyone constructing `SubscriptionParams`, will need updating), so it probably wants to land alongside a major version bump — but the resulting API is much more idiomatic C++ and removes pointless allocations.
