[Bug]: plugin fails for calc(infinity * 1s)
### Describe the bug

Running the plugin fails on css containing a calculation using constant values. (See: https://developer.mozilla.org/en-US/docs/Web/CSS/calc-constant)

### Expected behaviour

I'd expect the plugin to support calc-constant values or to at least not touch calculations it can't optimize to not cause such issues.

### Steps to reproduce

Either create a new nuxt app and use `calc(infinity * 1px)` somewhere inside the css and try to run a build or:

1. Check out https://github.com/SchwarzIT/onyx
2. Run `pnpm i`
3. Go into the file `packages/nuxt/src/module.ts` and comment out the line disabling calc for cssnano:
<img width="651" alt="image" src="https://github.com/postcss/postcss-calc/assets/95471369/737a7180-2bf4-45a5-a832-dc0a8f27e5cc">

4. Run `pnpm run build:all`
5. cd into `packages/nuxt`
6. Run `pnpm run dev:build`

You will see vite starting to build the client and then just hanging up because the calc plugin isn't able to work with the expression `calc(infinity * 1s)` used inside `packages/sit-onyx/src/components/OnyxInput/OnyxInput.vue`.

### Version

9.0.1

### Environment

```shell
System:
    OS: macOS 14.5
    CPU: (10) arm64 Apple M1 Max
    Memory: 932.81 MB / 32.00 GB
    Shell: 5.9 - /bin/zsh
```


### Package details

```shell
@sit-onyx/nuxt@0.0.1-alpha.0 /Users/brockhoff/Documents/git/onyx/onyx/packages/nuxt
├─┬ @nuxt/devtools@1.3.3 -> ./../../node_modules/.pnpm/@nuxt+devtools@1.3.3_@unocss+reset@0.60.4_floating-vue@5.2.2_@nuxt+kit@3.11.2_rollup@4.18.0___r4qszsbagnoovha4wvyt6ueze4/node_modules/@nuxt/devtools
│ ├─┬ @nuxt/devtools-kit@1.3.3 -> ./../../node_modules/.pnpm/@nuxt+devtools-kit@1.3.3_nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+no_avlfaobvgiveoj46awszyk3iqu/node_modules/@nuxt/devtools-kit
│ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ @vue/devtools-applet@7.1.3 -> ./../../node_modules/.pnpm/@vue+devtools-applet@7.1.3_@unocss+reset@0.60.4_floating-vue@5.2.2_@nuxt+kit@3.11.2_rollup@4._ahuuq4bj56ct6lsj7iqpe2o5ra/node_modules/@vue/devtools-applet
│ │ ├─┬ splitpanes@3.1.5 -> ./../../node_modules/.pnpm/splitpanes@3.1.5/node_modules/splitpanes
│ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ └─┬ vite-plugin-dts@3.9.1 -> ./../../node_modules/.pnpm/vite-plugin-dts@3.9.1_@types+node@20.14.2_rollup@4.18.0_typescript@5.4.5_vite@5.2.12_@types+n_m4xikistgp2o47hckx5lomswpe/node_modules/vite-plugin-dts
│ │   └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │     └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ @vue/devtools-core@7.1.3 -> ./../../node_modules/.pnpm/@vue+devtools-core@7.1.3_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.3_smy4ankrvzu44ri6qlajbql6km/node_modules/@vue/devtools-core
│ │ └─┬ vite-hot-client@0.2.3 -> ./../../node_modules/.pnpm/vite-hot-client@0.2.3_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0_/node_modules/vite-hot-client
│ │   └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │     └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ nitropack@2.9.6 -> ./../../node_modules/.pnpm/nitropack@2.9.6_@opentelemetry+api@1.8.0_encoding@0.1.13/node_modules/nitropack
│ │ └─┬ rollup-plugin-visualizer@5.12.0 -> ./../../node_modules/.pnpm/rollup-plugin-visualizer@5.12.0_rollup@4.18.0/node_modules/rollup-plugin-visualizer
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ unocss@0.60.4 -> ./../../node_modules/.pnpm/unocss@0.60.4_postcss@8.4.38_rollup@4.18.0_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0_/node_modules/unocss
│ │ ├─┬ @unocss/astro@0.60.4 -> ./../../node_modules/.pnpm/@unocss+astro@0.60.4_rollup@4.18.0_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0_/node_modules/@unocss/astro
│ │ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ ├─┬ @unocss/postcss@0.60.4 -> ./../../node_modules/.pnpm/@unocss+postcss@0.60.4_postcss@8.4.38/node_modules/@unocss/postcss
│ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ ├─┬ @unocss/vite@0.60.4 -> ./../../node_modules/.pnpm/@unocss+vite@0.60.4_rollup@4.18.0_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0_/node_modules/@unocss/vite
│ │ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ vite-plugin-inspect@0.8.4 -> ./../../node_modules/.pnpm/vite-plugin-inspect@0.8.4_@nuxt+kit@3.11.2_rollup@4.18.0__rollup@4.18.0_vite@5.2.12_@types+no_mowh2pif45rehdsvzgub6veaea/node_modules/vite-plugin-inspect
│ │ ├─┬ splitpanes@3.1.5 -> ./../../node_modules/.pnpm/splitpanes@3.1.5/node_modules/splitpanes
│ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ vite-plugin-vue-inspector@5.1.2 -> ./../../node_modules/.pnpm/vite-plugin-vue-inspector@5.1.2_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0_/node_modules/vite-plugin-vue-inspector
│ │ ├─┬ @vue/babel-plugin-jsx@1.2.2 -> ./../../node_modules/.pnpm/@vue+babel-plugin-jsx@1.2.2_@babel+core@7.24.6/node_modules/@vue/babel-plugin-jsx
│ │ │ └─┬ @vue/babel-plugin-resolve-type@1.2.2 -> ./../../node_modules/.pnpm/@vue+babel-plugin-resolve-type@1.2.2_@babel+core@7.24.6/node_modules/@vue/babel-plugin-resolve-type
│ │ │   └─┬ @vue/compiler-sfc@3.4.27 -> ./../../node_modules/.pnpm/@vue+compiler-sfc@3.4.27/node_modules/@vue/compiler-sfc
│ │ │     └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ └─┬ vue-virtual-scroller@2.0.0-beta.8 -> ./../../node_modules/.pnpm/vue-virtual-scroller@2.0.0-beta.8_vue@3.4.27_typescript@5.4.5_/node_modules/vue-virtual-scroller
│   └─┬ autoprefixer@10.4.19 invalid: "^9.7.5" from ../../node_modules/.pnpm/vue-virtual-scroller@2.0.0-beta.8_vue@3.4.27_typescript@5.4.5_/node_modules/vue-virtual-scroller, "^9.7.5" from ../../node_modules/.pnpm/vue-virtual-scroller@2.0.0-beta.8_vue@3.4.27_typescript@5.4.5_/node_modules/vue-virtual-scroller, "^9.7.5" from ../../node_modules/.pnpm/vue-resize@2.0.0-alpha.1_vue@3.4.27_typescript@5.4.5_/node_modules/vue-resize -> ./../../node_modules/.pnpm/autoprefixer@10.4.19_postcss@8.4.38/node_modules/autoprefixer
│     └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
├─┬ @nuxt/kit@3.11.2 -> ./../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit
│ ├─┬ unbuild@2.0.0 invalid: "latest" from ../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit, "latest" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "latest" from ../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils, "latest" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "latest" from ../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit, "latest" from ../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils, "^1.2.1" from ../../node_modules/.pnpm/consola@3.2.3/node_modules/consola, "^1.1.2" from ../../node_modules/.pnpm/hookable@5.5.3/node_modules/hookable, "latest" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "^1.2.1" from ../../node_modules/.pnpm/ohash@1.1.3/node_modules/ohash, "^1.2.1" from ../../node_modules/.pnpm/perfect-debounce@1.0.0/node_modules/perfect-debounce, "latest" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "^1.2.1" from ../../node_modules/.pnpm/consola@3.2.3/node_modules/consola -> ./../../node_modules/.pnpm/unbuild@2.0.0_sass@1.77.4_typescript@5.4.5_vue-tsc@2.0.19_typescript@5.4.5_/node_modules/unbuild
│ │ └─┬ mkdist@1.5.1 -> ./../../node_modules/.pnpm/mkdist@1.5.1_sass@1.77.4_typescript@5.4.5_vue-tsc@2.0.19_typescript@5.4.5_/node_modules/mkdist
│ │   ├─┬ autoprefixer@10.4.19 -> ./../../node_modules/.pnpm/autoprefixer@10.4.19_postcss@8.4.38/node_modules/autoprefixer
│ │   │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   ├─┬ cssnano@7.0.2 -> ./../../node_modules/.pnpm/cssnano@7.0.2_postcss@8.4.38/node_modules/cssnano
│ │   │ ├─┬ cssnano-preset-default@7.0.2 -> ./../../node_modules/.pnpm/cssnano-preset-default@7.0.2_postcss@8.4.38/node_modules/cssnano-preset-default
│ │   │ │ ├─┬ css-declaration-sorter@7.2.0 -> ./../../node_modules/.pnpm/css-declaration-sorter@7.2.0_postcss@8.4.38/node_modules/css-declaration-sorter
│ │   │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ cssnano-utils@5.0.0 -> ./../../node_modules/.pnpm/cssnano-utils@5.0.0_postcss@8.4.38/node_modules/cssnano-utils
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-calc@10.0.0 -> ./../../node_modules/.pnpm/postcss-calc@10.0.0_postcss@8.4.38/node_modules/postcss-calc
│ │   │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-colormin@7.0.0 -> ./../../node_modules/.pnpm/postcss-colormin@7.0.0_postcss@8.4.38/node_modules/postcss-colormin
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-convert-values@7.0.0 -> ./../../node_modules/.pnpm/postcss-convert-values@7.0.0_postcss@8.4.38/node_modules/postcss-convert-values
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-discard-comments@7.0.0 -> ./../../node_modules/.pnpm/postcss-discard-comments@7.0.0_postcss@8.4.38/node_modules/postcss-discard-comments
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-discard-duplicates@7.0.0 -> ./../../node_modules/.pnpm/postcss-discard-duplicates@7.0.0_postcss@8.4.38/node_modules/postcss-discard-duplicates
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-discard-empty@7.0.0 -> ./../../node_modules/.pnpm/postcss-discard-empty@7.0.0_postcss@8.4.38/node_modules/postcss-discard-empty
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-discard-overridden@7.0.0 -> ./../../node_modules/.pnpm/postcss-discard-overridden@7.0.0_postcss@8.4.38/node_modules/postcss-discard-overridden
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-merge-longhand@7.0.1 -> ./../../node_modules/.pnpm/postcss-merge-longhand@7.0.1_postcss@8.4.38/node_modules/postcss-merge-longhand
│ │   │ │ │ ├── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └─┬ stylehacks@7.0.1 -> ./../../node_modules/.pnpm/stylehacks@7.0.1_postcss@8.4.38/node_modules/stylehacks
│ │   │ │ │   ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │   │ │ │   │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │   └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-merge-rules@7.0.1 -> ./../../node_modules/.pnpm/postcss-merge-rules@7.0.1_postcss@8.4.38/node_modules/postcss-merge-rules
│ │   │ │ │ ├─┬ cssnano-utils@5.0.0 -> ./../../node_modules/.pnpm/cssnano-utils@5.0.0_postcss@8.4.38/node_modules/cssnano-utils
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-minify-font-values@7.0.0 -> ./../../node_modules/.pnpm/postcss-minify-font-values@7.0.0_postcss@8.4.38/node_modules/postcss-minify-font-values
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-minify-gradients@7.0.0 -> ./../../node_modules/.pnpm/postcss-minify-gradients@7.0.0_postcss@8.4.38/node_modules/postcss-minify-gradients
│ │   │ │ │ ├─┬ cssnano-utils@5.0.0 -> ./../../node_modules/.pnpm/cssnano-utils@5.0.0_postcss@8.4.38/node_modules/cssnano-utils
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-minify-params@7.0.0 -> ./../../node_modules/.pnpm/postcss-minify-params@7.0.0_postcss@8.4.38/node_modules/postcss-minify-params
│ │   │ │ │ ├─┬ cssnano-utils@5.0.0 -> ./../../node_modules/.pnpm/cssnano-utils@5.0.0_postcss@8.4.38/node_modules/cssnano-utils
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-minify-selectors@7.0.1 -> ./../../node_modules/.pnpm/postcss-minify-selectors@7.0.1_postcss@8.4.38/node_modules/postcss-minify-selectors
│ │   │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-charset@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-charset@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-charset
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-display-values@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-display-values@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-display-values
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-positions@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-positions@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-positions
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-repeat-style@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-repeat-style@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-repeat-style
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-string@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-string@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-string
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-timing-functions@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-timing-functions@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-timing-functions
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-unicode@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-unicode@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-unicode
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-url@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-url@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-url
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-normalize-whitespace@7.0.0 -> ./../../node_modules/.pnpm/postcss-normalize-whitespace@7.0.0_postcss@8.4.38/node_modules/postcss-normalize-whitespace
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-ordered-values@7.0.0 -> ./../../node_modules/.pnpm/postcss-ordered-values@7.0.0_postcss@8.4.38/node_modules/postcss-ordered-values
│ │   │ │ │ ├─┬ cssnano-utils@5.0.0 -> ./../../node_modules/.pnpm/cssnano-utils@5.0.0_postcss@8.4.38/node_modules/cssnano-utils
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-reduce-initial@7.0.0 -> ./../../node_modules/.pnpm/postcss-reduce-initial@7.0.0_postcss@8.4.38/node_modules/postcss-reduce-initial
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-reduce-transforms@7.0.0 -> ./../../node_modules/.pnpm/postcss-reduce-transforms@7.0.0_postcss@8.4.38/node_modules/postcss-reduce-transforms
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-svgo@7.0.1 -> ./../../node_modules/.pnpm/postcss-svgo@7.0.1_postcss@8.4.38/node_modules/postcss-svgo
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ ├─┬ postcss-unique-selectors@7.0.1 -> ./../../node_modules/.pnpm/postcss-unique-selectors@7.0.1_postcss@8.4.38/node_modules/postcss-unique-selectors
│ │   │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │   │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   ├─┬ postcss-nested@6.0.1 -> ./../../node_modules/.pnpm/postcss-nested@6.0.1_postcss@8.4.38/node_modules/postcss-nested
│ │   │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │   │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ vite@5.2.12 invalid: "5.2.8" from ../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit, "5.2.8" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "5.2.8" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "5.2.8" from ../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit, "^4.3.9" from ../../node_modules/.pnpm/floating-vue@5.2.2_@nuxt+kit@3.11.2_rollup@4.18.0__vue@3.4.27_typescript@5.4.5_/node_modules/floating-vue, "^4.2.1" from ../../node_modules/.pnpm/hookable@5.5.3/node_modules/hookable, "5.2.8" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "5.2.8" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ └─┬ vitest@1.6.0 invalid: "1.4.0" from ../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit, "1.4.0" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "1.4.0" from ../../node_modules/.pnpm/@nuxt+kit@3.11.2_rollup@4.18.0/node_modules/@nuxt/kit, "^0.32.2" from ../../node_modules/.pnpm/consola@3.2.3/node_modules/consola, "^0.29.8" from ../../node_modules/.pnpm/hookable@5.5.3/node_modules/hookable, "^0.34.6" from ../../node_modules/.pnpm/image-meta@0.2.0/node_modules/image-meta, "^0.34.6" from ../../node_modules/.pnpm/local-pkg@0.5.0/node_modules/local-pkg, "1.4.0" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "^0.34.1" from ../../node_modules/.pnpm/ohash@1.1.3/node_modules/ohash, "^0.31.0" from ../../node_modules/.pnpm/perfect-debounce@1.0.0/node_modules/perfect-debounce, "^0.32.2" from ../../node_modules/.pnpm/consola@3.2.3/node_modules/consola, "^0.34.2" from ../../node_modules/.pnpm/unbuild@2.0.0_sass@1.77.4_typescript@5.4.5_vue-tsc@2.0.19_typescript@5.4.5_/node_modules/unbuild, "^0.31.1" from ../../node_modules/.pnpm/unctx@2.3.1/node_modules/unctx -> ./../../node_modules/.pnpm/vitest@1.6.0_@types+node@20.14.2_jsdom@24.1.0_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vitest
│   ├─┬ vite-node@1.6.0 -> ./../../node_modules/.pnpm/vite-node@1.6.0_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite-node
│   │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│   │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│   └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│     └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
├─┬ @nuxt/module-builder@0.7.0 -> ./../../node_modules/.pnpm/@nuxt+module-builder@0.7.0_@nuxt+kit@3.11.2_rollup@4.18.0__nuxi@3.11.1_sass@1.77.4_typescript_2kjme4buuz22hceirfoallukby/node_modules/@nuxt/module-builder
│ └─┬ vue@3.4.27 invalid: "3.4.21" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "3.4.21" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "3.4.21" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema -> ./../../node_modules/.pnpm/vue@3.4.27_typescript@5.4.5/node_modules/vue
│   └─┬ @vue/compiler-sfc@3.4.27 -> ./../../node_modules/.pnpm/@vue+compiler-sfc@3.4.27/node_modules/@vue/compiler-sfc
│     └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
├─┬ @nuxt/schema@3.11.2 -> ./../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema
│ ├─┬ @vitejs/plugin-vue-jsx@3.1.0 -> ./../../node_modules/.pnpm/@vitejs+plugin-vue-jsx@3.1.0_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser_xthkfiqrlcvdqkh3xrix3paxcy/node_modules/@vitejs/plugin-vue-jsx
│ │ └─┬ vite@5.2.12 invalid: "^4.5.0" from ../../node_modules/.pnpm/@vitejs+plugin-vue-jsx@3.1.0_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser_xthkfiqrlcvdqkh3xrix3paxcy/node_modules/@vitejs/plugin-vue-jsx -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ ├─┬ @vitejs/plugin-vue@5.0.5 invalid: "5.0.4" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "5.0.4" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "^4.2.3" from ../../node_modules/.pnpm/floating-vue@5.2.2_@nuxt+kit@3.11.2_rollup@4.18.0__vue@3.4.27_typescript@5.4.5_/node_modules/floating-vue, "5.0.4" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt, "5.0.4" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "5.0.4" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "5.0.4" from ../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt -> ./../../node_modules/.pnpm/@vitejs+plugin-vue@5.0.5_vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.3_wea4bwhjdn3d4h5i6tchcm2s54/node_modules/@vitejs/plugin-vue
│ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ └─┬ @vue/compiler-sfc@3.4.27 invalid: "3.4.21" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "3.4.21" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema, "3.4.21" from ../../node_modules/.pnpm/@nuxt+schema@3.11.2_rollup@4.18.0/node_modules/@nuxt/schema -> ./../../node_modules/.pnpm/@vue+compiler-sfc@3.4.27/node_modules/@vue/compiler-sfc
│   ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│   │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│   └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
├─┬ @nuxt/test-utils@3.13.1 -> ./../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils
│ ├─┬ rollup@4.18.0 invalid: "4.17.2" from ../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils, "4.17.2" from ../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils, "^2.45.2" from ../../node_modules/.pnpm/vue-virtual-scroller@2.0.0-beta.8_vue@3.4.27_typescript@5.4.5_/node_modules/vue-virtual-scroller, "4.12.1" from ../../node_modules/.pnpm/magic-regexp@0.8.0/node_modules/magic-regexp, "^3.29.4" from ../../node_modules/.pnpm/vue-router@4.3.2_vue@3.4.27_typescript@5.4.5_/node_modules/vue-router, "^3.29.4" from ../../node_modules/.pnpm/magic-string@0.30.10/node_modules/magic-string -> ./../../node_modules/.pnpm/rollup@4.18.0/node_modules/rollup
│ │ ├─┬ eslint-plugin-vue@9.26.0 invalid: "^7.4.0" from ../../node_modules/.pnpm/vue-resize@2.0.0-alpha.1_vue@3.4.27_typescript@5.4.5_/node_modules/vue-resize, "^7.4.0" from ../../node_modules/.pnpm/vue-resize@2.0.0-alpha.1_vue@3.4.27_typescript@5.4.5_/node_modules/vue-resize -> ./../../node_modules/.pnpm/eslint-plugin-vue@9.26.0_eslint@8.57.0/node_modules/eslint-plugin-vue
│ │ │ └─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ └─┬ vitepress@1.2.3 -> ./../../node_modules/.pnpm/vitepress@1.2.3_@algolia+client-search@4.23.2_@types+node@20.14.2_@types+react@18.3.3_postcss_g44hvyz4hrf73mi2gurzwbv5a4/node_modules/vitepress
│ │   ├── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │   └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │     └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ └─┬ vite@5.2.12 invalid: "5.2.11" from ../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils, "5.2.11" from ../../node_modules/.pnpm/@nuxt+test-utils@3.13.1_@playwright+test@1.44.1_h3@1.11.1_jsdom@24.1.0_nitropack@2.9.6_@opent_t3hoj4uleem2azlclv6yxxikti/node_modules/@nuxt/test-utils -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
├─┬ nuxt@3.11.2 -> ./../../node_modules/.pnpm/nuxt@3.11.2_@opentelemetry+api@1.8.0_@parcel+watcher@2.4.1_@types+node@20.14.2_@unocss+reset@_rumj7wi6j3ahl67th2ak75ynqa/node_modules/nuxt
│ ├─┬ @nuxt/vite-builder@3.11.2 -> ./../../node_modules/.pnpm/@nuxt+vite-builder@3.11.2_@types+node@20.14.2_eslint@9.4.0_optionator@0.9.4_rollup@4.18.0_sas_62cp7udrz4ldf3ngr3tddphzam/node_modules/@nuxt/vite-builder
│ │ ├─┬ autoprefixer@10.4.19 -> ./../../node_modules/.pnpm/autoprefixer@10.4.19_postcss@8.4.38/node_modules/autoprefixer
│ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ ├─┬ cssnano@6.1.2 -> ./../../node_modules/.pnpm/cssnano@6.1.2_postcss@8.4.38/node_modules/cssnano
│ │ │ ├─┬ cssnano-preset-default@6.1.2 -> ./../../node_modules/.pnpm/cssnano-preset-default@6.1.2_postcss@8.4.38/node_modules/cssnano-preset-default
│ │ │ │ ├─┬ css-declaration-sorter@7.2.0 -> ./../../node_modules/.pnpm/css-declaration-sorter@7.2.0_postcss@8.4.38/node_modules/css-declaration-sorter
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ cssnano-utils@4.0.2 -> ./../../node_modules/.pnpm/cssnano-utils@4.0.2_postcss@8.4.38/node_modules/cssnano-utils
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-calc@9.0.1 -> ./../../node_modules/.pnpm/postcss-calc@9.0.1_postcss@8.4.38/node_modules/postcss-calc
│ │ │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-colormin@6.1.0 -> ./../../node_modules/.pnpm/postcss-colormin@6.1.0_postcss@8.4.38/node_modules/postcss-colormin
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-convert-values@6.1.0 -> ./../../node_modules/.pnpm/postcss-convert-values@6.1.0_postcss@8.4.38/node_modules/postcss-convert-values
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-discard-comments@6.0.2 -> ./../../node_modules/.pnpm/postcss-discard-comments@6.0.2_postcss@8.4.38/node_modules/postcss-discard-comments
│ │ │ │ │ ├─┬ postcss-scss@4.0.9 -> ./../../node_modules/.pnpm/postcss-scss@4.0.9_postcss@8.4.38/node_modules/postcss-scss
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-discard-duplicates@6.0.3 -> ./../../node_modules/.pnpm/postcss-discard-duplicates@6.0.3_postcss@8.4.38/node_modules/postcss-discard-duplicates
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-discard-empty@6.0.3 -> ./../../node_modules/.pnpm/postcss-discard-empty@6.0.3_postcss@8.4.38/node_modules/postcss-discard-empty
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-discard-overridden@6.0.2 -> ./../../node_modules/.pnpm/postcss-discard-overridden@6.0.2_postcss@8.4.38/node_modules/postcss-discard-overridden
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-merge-longhand@6.0.5 -> ./../../node_modules/.pnpm/postcss-merge-longhand@6.0.5_postcss@8.4.38/node_modules/postcss-merge-longhand
│ │ │ │ │ ├── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └─┬ stylehacks@6.1.1 -> ./../../node_modules/.pnpm/stylehacks@6.1.1_postcss@8.4.38/node_modules/stylehacks
│ │ │ │ │   ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │ │ │ │   │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │   └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-merge-rules@6.1.1 -> ./../../node_modules/.pnpm/postcss-merge-rules@6.1.1_postcss@8.4.38/node_modules/postcss-merge-rules
│ │ │ │ │ ├─┬ cssnano-utils@4.0.2 -> ./../../node_modules/.pnpm/cssnano-utils@4.0.2_postcss@8.4.38/node_modules/cssnano-utils
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ ├─┬ postcss-discard-comments@6.0.2 invalid: "^7.0.0" from ../../node_modules/.pnpm/postcss-merge-rules@7.0.1_postcss@8.4.38/node_modules/postcss-merge-rules -> ./../../node_modules/.pnpm/postcss-discard-comments@6.0.2_postcss@8.4.38/node_modules/postcss-discard-comments
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-minify-font-values@6.1.0 -> ./../../node_modules/.pnpm/postcss-minify-font-values@6.1.0_postcss@8.4.38/node_modules/postcss-minify-font-values
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-minify-gradients@6.0.3 -> ./../../node_modules/.pnpm/postcss-minify-gradients@6.0.3_postcss@8.4.38/node_modules/postcss-minify-gradients
│ │ │ │ │ ├─┬ cssnano-utils@4.0.2 -> ./../../node_modules/.pnpm/cssnano-utils@4.0.2_postcss@8.4.38/node_modules/cssnano-utils
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-minify-params@6.1.0 -> ./../../node_modules/.pnpm/postcss-minify-params@6.1.0_postcss@8.4.38/node_modules/postcss-minify-params
│ │ │ │ │ ├─┬ cssnano-utils@4.0.2 -> ./../../node_modules/.pnpm/cssnano-utils@4.0.2_postcss@8.4.38/node_modules/cssnano-utils
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-minify-selectors@6.0.4 -> ./../../node_modules/.pnpm/postcss-minify-selectors@6.0.4_postcss@8.4.38/node_modules/postcss-minify-selectors
│ │ │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-charset@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-charset@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-charset
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-display-values@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-display-values@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-display-values
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-positions@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-positions@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-positions
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-repeat-style@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-repeat-style@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-repeat-style
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-string@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-string@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-string
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-timing-functions@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-timing-functions@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-timing-functions
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-unicode@6.1.0 -> ./../../node_modules/.pnpm/postcss-normalize-unicode@6.1.0_postcss@8.4.38/node_modules/postcss-normalize-unicode
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-url@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-url@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-url
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-normalize-whitespace@6.0.2 -> ./../../node_modules/.pnpm/postcss-normalize-whitespace@6.0.2_postcss@8.4.38/node_modules/postcss-normalize-whitespace
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-ordered-values@6.0.2 -> ./../../node_modules/.pnpm/postcss-ordered-values@6.0.2_postcss@8.4.38/node_modules/postcss-ordered-values
│ │ │ │ │ ├─┬ cssnano-utils@4.0.2 -> ./../../node_modules/.pnpm/cssnano-utils@4.0.2_postcss@8.4.38/node_modules/cssnano-utils
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-reduce-initial@6.1.0 -> ./../../node_modules/.pnpm/postcss-reduce-initial@6.1.0_postcss@8.4.38/node_modules/postcss-reduce-initial
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-reduce-transforms@6.0.2 -> ./../../node_modules/.pnpm/postcss-reduce-transforms@6.0.2_postcss@8.4.38/node_modules/postcss-reduce-transforms
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-svgo@6.0.3 -> ./../../node_modules/.pnpm/postcss-svgo@6.0.3_postcss@8.4.38/node_modules/postcss-svgo
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ ├─┬ postcss-unique-selectors@6.0.4 -> ./../../node_modules/.pnpm/postcss-unique-selectors@6.0.4_postcss@8.4.38/node_modules/postcss-unique-selectors
│ │ │ │ │ ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
│ │ │ │ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ ├── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ ├─┬ rollup-plugin-visualizer@5.12.0 -> ./../../node_modules/.pnpm/rollup-plugin-visualizer@5.12.0_rollup@4.18.0/node_modules/rollup-plugin-visualizer
│ │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ ├─┬ vite-plugin-checker@0.6.4 -> ./../../node_modules/.pnpm/vite-plugin-checker@0.6.4_eslint@9.4.0_optionator@0.9.4_typescript@5.4.5_vite@5.2.12_@types+n_mxym5yfcbwfaduc4xizx3jyamm/node_modules/vite-plugin-checker
│ │ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ │ └─┬ vite@5.2.12 -> ./../../node_modules/.pnpm/vite@5.2.12_@types+node@20.14.2_sass@1.77.4_stylus@0.57.0_terser@5.31.0/node_modules/vite
│ │   └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
│ └─┬ unplugin-vue-router@0.7.0 -> ./../../node_modules/.pnpm/unplugin-vue-router@0.7.0_rollup@4.18.0_vue-router@4.3.2_vue@3.4.27_typescript@5.4.5___vue@3.4.27_typescript@5.4.5_/node_modules/unplugin-vue-router
│   └─┬ @vue-macros/common@1.10.4 -> ./../../node_modules/.pnpm/@vue-macros+common@1.10.4_rollup@4.18.0_vue@3.4.27_typescript@5.4.5_/node_modules/@vue-macros/common
│     └─┬ @vue/compiler-sfc@3.4.27 -> ./../../node_modules/.pnpm/@vue+compiler-sfc@3.4.27/node_modules/@vue/compiler-sfc
│       └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
└─┬ sit-onyx@1.0.0-alpha.122 invalid: "workspace:^" from the root project -> ./../sit-onyx
  └─┬ eslint-plugin-vue-scoped-css@2.8.0 -> ./../../node_modules/.pnpm/eslint-plugin-vue-scoped-css@2.8.0_eslint@9.4.0_vue-eslint-parser@9.4.2_eslint@9.4.0_/node_modules/eslint-plugin-vue-scoped-css
    ├─┬ postcss-safe-parser@6.0.0 -> ./../../node_modules/.pnpm/postcss-safe-parser@6.0.0_postcss@8.4.38/node_modules/postcss-safe-parser
    │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
    ├─┬ postcss-scss@4.0.9 -> ./../../node_modules/.pnpm/postcss-scss@4.0.9_postcss@8.4.38/node_modules/postcss-scss
    │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
    ├─┬ postcss-selector-parser@6.1.0 -> ./../../node_modules/.pnpm/postcss-selector-parser@6.1.0/node_modules/postcss-selector-parser
    │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
    ├─┬ postcss-styl@0.12.3 -> ./../../node_modules/.pnpm/postcss-styl@0.12.3/node_modules/postcss-styl
    │ ├─┬ postcss-nested@6.0.1 invalid: "^5.0.4" from ../../node_modules/.pnpm/postcss-styl@0.12.3/node_modules/postcss-styl -> ./../../node_modules/.pnpm/postcss-nested@6.0.1_postcss@8.4.38/node_modules/postcss-nested
    │ │ └── postcss@8.4.38 deduped -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
    │ └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
    └── postcss@8.4.38 -> ./../../node_modules/.pnpm/postcss@8.4.38/node_modules/postcss
```


### Additional context

I got here as I encountered a bug within a Nuxt Js app using css with the statement `calc(infinity *1s)`. It worked during development but at build time vite just hung up so I investigated further. Turns out nuxt uses postcss with nanocss by default. Nanocss again includes this plugin which causes the issue.

It would be really great if the plugin could support these relatively new but stable constants. Thanks
