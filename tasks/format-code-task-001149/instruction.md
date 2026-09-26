Audio selection is shared by the background page, dictionary display, and Anki export, so a malformed URI or a stale cached result can make a configured source appear to work while silently playing the wrong entry. Please make the audio URI and selection behavior consistent across the supported source modes.

The URI builder must produce the JapanesePod101 URL with kanji and kana query parameters only when their values are non-empty. When an expression is entirely kana and no reading is supplied, use that expression as the kana parameter and omit kanji; when both fields are empty, return the endpoint with an empty query string. Values must be percent-encoded without changing the parameter names or their order.

For text-to-speech and text-to-speech-reading, require a non-empty configured voice and return no URI when it is absent or empty. The normal mode speaks the expression. The reading mode speaks the reading when present and otherwise falls back to the expression. Text and voice values must be encoded in the returned tts URI.

Unknown source names and a custom source without a string URL must yield null rather than an unusable URI. Custom URL templates replace known definition properties with their percent-encoded values independently, while preserving placeholders for unknown properties so users can diagnose an incomplete template.

Keep URL normalization compatible with the existing scrapers: empty and already absolute URLs (including data URLs) are returned unchanged; protocol-relative URLs inherit the base scheme; root-relative URLs resolve against the base origin; and other relative paths resolve beneath the supplied base path.

AudioSystem.getDefinitionAudio must evaluate sources in the supplied order, skip sources whose URI is null, continue after URI creation or playback construction failures, and return the first playable result with its URI and zero-based source index. If every source is unavailable or fails, reject with the exact message Could not create audio.

When caching is enabled, an identical definition request with the same effective source details must reuse the same audio object. A change to those effective details must invalidate a stale entry, and a failed attempt must not poison a later request for the same definition. Preserve the existing public return shape and behavior for successful uncached requests.
