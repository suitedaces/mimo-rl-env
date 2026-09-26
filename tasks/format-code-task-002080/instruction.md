crossorigin has invalid value "true"
I believe there is an error at [this line](https://github.com/nuxt-community/google-fonts-module/blob/b9c59eafacab263852a7579743081e03536c52d1/lib/module.js#L95).

It raises an error with html-validator:
> error  Attribute "crossorigin" has invalid value "true"  attribute-allowed-values

The rendered element is:
`<link data-n-head="ssr" data-hid="gf-preconnect" rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="true">`

It should be:
`<link data-n-head="ssr" data-hid="gf-preconnect" rel="preconnect" href="https://fonts.gstatic.com/" crossorigin>`
