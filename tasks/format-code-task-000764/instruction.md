## iframeResizer crashes on load when `window.jQuery` is declared but undefined

I'm using iframe-resizer on a page that doesn't depend on jQuery — I'm just using the native `window.iFrameResize` API. The page does, however, load a couple of other third-party scripts, and one of them declares `window.jQuery` on the global object but leaves it as `undefined` (it's a shim that conditionally exposes jQuery only if some other condition is met).

As soon as `iframeResizer.js` is included on the page, it blows up during the initial script execution, before I ever get a chance to call `iFrameResize(...)`. Nothing on the page works after that point.

If I remove the offending shim (so that `jQuery` isn't a property on `window` at all), iframeResizer loads fine and the native API works as expected. So it really does look like the script is unhappy specifically when `window.jQuery` exists as a name but doesn't actually point at a usable jQuery object.

I'd expect the library to just skip its jQuery integration in this situation and keep working through the native API. Folks using iframeResizer without jQuery (or in environments where some other code has nulled it out / set it to undefined) shouldn't have to monkey-patch the global scope just to load the script.

Repro is basically:

```html
<script>
  // simulate a shim / polyfill that defines the name but not a value
  window.jQuery = undefined;
</script>
<script src="src/iframeResizer.js"></script>
<script>
  // never gets here
  iFrameResize({ log: true }, '#myIframe');
</script>
```

Could the jQuery detection be relaxed so that "the name exists on window but the value isn't actually a jQuery" is treated the same as "no jQuery at all"?
