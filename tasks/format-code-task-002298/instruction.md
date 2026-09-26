incorrect reduction of subtraction css-variable from zero
While https://github.com/postcss/postcss-calc/issues/88 is fixed by https://github.com/postcss/postcss-calc/pull/93  ,  this case still has bug:
`calc(0px - (var(--foo, 4px) / 2))`
is reduced into:
`calc(var(--foo, 4px)/2)`
