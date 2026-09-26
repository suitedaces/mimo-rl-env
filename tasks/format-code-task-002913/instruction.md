## Output isn't written to `file.value` when using vfile v5

I'm trying to upgrade my project to `vfile@5` and use it with `unified`. After processing, the resulting file doesn't carry the stringified output where vfile v5 documents it.

Rough repro:

```js
import {unified} from 'unified'
import vfile from 'vfile' // v5
// some processor with a Parser + Compiler, e.g. remark
import remarkParse from 'remark-parse'
import remarkStringify from 'remark-stringify'

const file = vfile('# hi')

const out = await unified()
  .use(remarkParse)
  .use(remarkStringify)
  .process(file)

console.log(out.value)    // undefined / empty
console.log(String(out))  // also not what I expect on a v5 vfile
```

On `vfile@4` the same pipeline works because everything reads from `.contents`. On `vfile@5` the file API exposes `.value` instead, and that's what I (and anything else that's been updated for v5) reach for after `process()` returns — but it's empty.

It looks like `unified` only knows about the old vfile shape on the way out, so anyone moving to `vfile@5` loses the processed result unless they reach into legacy fields. It'd be great if `unified` worked with both vfile v4 and v5 so users can upgrade vfile independently.
