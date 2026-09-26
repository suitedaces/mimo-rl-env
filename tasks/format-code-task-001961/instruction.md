## `bson_validate_with_error_and_offset` returns false but leaves `error` / `offset` uninitialized for some invalid inputs

I'm using `bson_validate_with_error_and_offset` to vet untrusted BSON buffers before handing them to the rest of my pipeline. My code roughly looks like:

```c
bson_t doc;
bson_init_static (&doc, buf, buf_len);

bson_error_t err;
size_t off;
if (!bson_validate_with_error_and_offset (&doc, BSON_VALIDATE_NONE, &off, &err)) {
    fprintf (stderr, "bson invalid at offset %zu: %s\n", off, err.message);
    return -1;
}
```

For most malformed inputs this works as expected — the function returns `false` and `err.message` / `off` describe what went wrong. But on certain inputs (some hand-crafted buffers that are bad right at the very start) the function still returns `false`, but the `bson_error_t` I pass in comes back looking empty/garbage and the offset I print is clearly uninitialized memory. So my log line is useless for those cases — I can tell something is wrong, but not what or where.

I'd expect that whenever `bson_validate_with_error_and_offset` reports failure, both the `error` and `offset` out-parameters are filled in with a meaningful description, regardless of where in the buffer the problem is.
