## CI `wasm_bindings` job is broken and `cargo test --all` blows up in `crates/testing`

I was trying to put up a PR and noticed the `wasm_bindings` job on GitHub Actions fails right away. The "Build rust-wasm-test" step is invoking

```
cargo run -p spacetimedb-cli -- build crates/modules/rust-wasm-test
```

but there is no `crates/modules/` directory anymore — the modules live under the top-level `modules/` directory now (`modules/rust-wasm-test`, `modules/benchmarks`, `modules/spacetimedb_quickstart`, all listed as workspace members in the root `Cargo.toml`). So the CLI bails out because it can't find the manifest. Looks like the CI workflow was just never updated when modules were moved.

I tried reproducing locally with `cargo test --all` and ran into a separate but related mess: the integration tests in `crates/testing` (`with_module` / `with_module_async` → `load_module`) panic when they try to read the compiled wasm. From poking at it, it seems the test harness is still resolving module paths and wasm artifact paths as if modules were under `crates/modules/`, so it ends up pointing at a file that doesn't exist and `std::fs::read(...).unwrap()` blows up.

A second thing I noticed while looking at this: the harness assumes every module's wasm artifact has the same fixed filename. But each module is its own crate with its own name, and `cargo build --target=wasm32-unknown-unknown --release` produces a wasm whose name comes from the crate name — so different modules produce differently-named `.wasm` files. As soon as you point it at, say, `benchmarks` instead of `rust-wasm-test`, the hardcoded filename won't match.

Also minor, but `modules/spacetimedb_quickstart` uses `snake_case` while the other entries under `modules/` are `kebab-case` — would be nice to make that consistent while we're cleaning this up.

It would be great to get CI green again and have the testing crate actually able to load module wasm from wherever the modules currently live.
