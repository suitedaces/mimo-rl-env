## Reading certain malformed/empty PDFs crashes the entire Node process

I'm using `muhammara` to process PDF files coming in from an upload pipeline, so I have to deal with whatever bytes the user throws at me — including files that turn out to be truncated, empty, or otherwise broken.

For most malformed inputs muhammara raises an error and I can handle it just fine. But for some files — in particular completely empty files, or files that look like they were cut off before any real content was written (think: a PDF where the upload died right after the header, or a 0-byte file that someone renamed to `.pdf`) — the whole Node process just dies. No exception, nothing I can `try/catch`, no error event. The process is simply gone.

Minimal repro that kills my worker:

```js
const muhammara = require('muhammara');
const fs = require('fs');

// e.g. a 0-byte file, or a file that ends before the PDF body really begins
fs.writeFileSync('/tmp/broken.pdf', '');

try {
  const reader = muhammara.createReader('/tmp/broken.pdf');
  // ...do stuff with reader
} catch (e) {
  // never gets here — the whole process is already dead
  console.error('caught:', e);
}
console.log('still alive?'); // never prints
```

Same thing happens with files that have a few bytes at the start but no actual PDF body / xref afterwards.

For a library that's meant to be usable on untrusted input this is pretty rough — one bad upload and the worker is gone. I'd expect muhammara to surface this as a normal failure (return value / throwable error) the same way it does for other malformed PDFs, instead of taking the process down with it.
