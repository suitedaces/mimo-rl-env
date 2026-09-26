## Feature request: allow whitelisting certain properties in `property-no-vendor-prefix`

I have `property-no-vendor-prefix` enabled and overall it's doing exactly what I want — flagging stuff like `-moz-columns` so I let autoprefixer handle it. The problem is there are a handful of properties where, for project-specific reasons, I really do want to keep the prefixed declaration in the source and don't want stylelint complaining about them.

Right now the rule is all-or-nothing: turn it on and every autoprefixable prefixed property gets flagged, turn it off and I lose the check for everything else. What I'd like is a way to tell the rule "check everything except these specific properties", similar to how a few other rules let you pass a list of names/patterns to skip.

Concretely, something along these lines in my config:

```css
a { -webkit-transform: scale(1); }   /* I want this to be allowed */
a { -moz-columns: 2; }               /* I want this to be allowed */
a { -webkit-user-select: none; }     /* this one should still be flagged */
```

Could `property-no-vendor-prefix` get a secondary option for this? Both plain strings and regex patterns would be ideal (matching against the unprefixed property name, so I don't have to enumerate every vendor variant).

I'd expect the secondary option key to be something like `ignoreProperties`.
