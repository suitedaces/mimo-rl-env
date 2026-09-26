## `parseInt` doesn't strip all ES5 whitespace chars even with es5-shim loaded

I'm cleaning up numeric strings that come from copy-pasting (user pastes a value from a webpage / spreadsheet and it ends up containing a non-breaking space `\u00A0` or other Unicode whitespace in front of the digits). My code does roughly:

```js
parseInt(rawValue, 10);
```

The ES5 spec for `parseInt` says it should skip leading `StrWhiteSpaceChar` — which is the full whitespace set (NBSP, the various `\u2000`-range spaces, `\u3000`, BOM, etc.), not just ASCII space / tab / newline. So I'd expect:

```js
parseInt('\u00A008', 10); // 8
parseInt('\u2003 0x16');  // 22
```

In several browsers `parseInt` only trims ASCII whitespace and returns `NaN` for these inputs. That's the kind of cross-engine inconsistency I'm pulling in es5-shim to fix, but loading the shim doesn't change the behavior here — `parseInt` still doesn't recognize the full whitespace set in those environments. Plain ASCII-space inputs (`parseInt(' 08')`) work fine, it's only the non-ASCII whitespace chars in the spec that aren't handled.

Could `parseInt` be brought in line with the ES5 spec's whitespace handling across browsers?
