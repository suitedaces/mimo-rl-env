### Loading a SentencePiece tokenizer with `byte_fallback` as a fast tokenizer hard-fails

After updating to a recent `transformers` version, converting a slow SentencePiece tokenizer that was trained with the `byte_fallback` option into its fast counterpart no longer works at all — it crashes outright instead of just notifying me about the limitation.

Minimal repro: take any sentencepiece model trained with `byte_fallback=True` in its trainer spec and try to load it as a fast tokenizer (e.g. `AutoTokenizer.from_pretrained(..., use_fast=True)`, which goes through `convert_slow_tokenizer`). The conversion blows up before it returns a tokenizer.

The message itself is informative — it explains that the fast tokenizer doesn't fully implement `byte_fallback` and that there can be unknown-token differences vs. the sentencepiece version. That's a real and useful caveat. But making it a hard error means I can't load the tokenizer at all, even when I'm fine with the difference in behavior for my use case (and in earlier versions this exact situation just printed a warning and proceeded).

I'd expect this to surface as a warning, not as an exception that aborts the conversion. Users who care can read the warning and decide; users who don't care still get a working fast tokenizer. Right now there's no way to opt in to "I know, just give me the fast tokenizer anyway" short of monkey-patching the conversion code.
