I want the public `compile(code: string, options?: object) -> object` API to compile Imba style `@keyframes` declarations into CSS in the returned `css.code` output.

For `compile("global css @keyframes blink\n\t0% o:1\n\t100% o:0", {sourcePath:"/tmp/example.imba", sourceId:"example"})`, `css.code` should contain `@keyframes blink` with `0%` and `100%` frames, and those frames should render the Imba `o` style shorthand as `opacity: 1;` and `opacity: 0;`.

For `compile("css .test\n\t@keyframes blink\n\t\tfrom o:0\n\t\tto o:1\n\t.item\n\t\tanimation-name: blink", {sourcePath:"/tmp/example.imba", sourceId:"example"})`, `css.code` should contain a scoped animation such as `@keyframes blink-test`, the `from` and `to` frames should render as CSS keyframe blocks, and the owning `.test` rule should expose `--animation-blink: blink-test;` so nested `animation-name: blink` resolves through `var(--animation-blink,blink)`.

The same `code` and `options` should produce the same `css.code` each time, and this compilation path should not write files, perform network calls, or mutate the input string.
