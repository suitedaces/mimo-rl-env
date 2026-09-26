Generation and speculative-decoding paths increasingly transform key/value caches instead of treating them as immutable tuples. The public `DynamicCache` and `EncoderDecoderCache` APIs need consistent bookkeeping when those transformations are composed, including models whose cached activations legitimately contain zeros.

Please harden these cache contracts without breaking the existing legacy/indexing and beam-search compatibility:

- Cropping a `DynamicCache` with a negative argument removes that many tokens from the end. If the request removes more tokens than are retained, the cache is empty rather than retaining a suffix or reporting a negative length; its public sequence-length metadata must agree with the tensors.
- Recombining batch splits must reject an empty split list with a `ValueError`, while normal split/recombine round trips preserve every layer's key/value tensors and sequence length.
- `EncoderDecoderCache.get_seq_length()` must report the self-attention token count from cache shape, independent of tensor values, and return a normal Python integer. Cross-attention update flags must likewise reflect that a cache is populated even when all cached values are zero.
- Encoder-decoder batch split/recombine must also work before cross-attention has been populated: preserve the self-attention cache and leave the cross-attention cache empty instead of indexing nonexistent layers.

Keep behavior outside these bookkeeping and transformation boundaries unchanged; callers should continue to use the documented public cache methods and legacy conversion paths.
