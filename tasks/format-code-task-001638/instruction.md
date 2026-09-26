## `split_on_silence` crashes when the input segment is entirely silent

I'm running `split_on_silence` over a batch of recordings to slice them into chunks. Most files work fine, but every once in a while one of the inputs is effectively silent end-to-end (e.g. a blank/empty recording, or a clip whose whole content sits below my `silence_thresh`). On those inputs the call blows up and takes down the whole batch.

Minimal repro:

```python
from pydub import AudioSegment
from pydub.silence import split_on_silence

# a segment that's entirely under the silence threshold
seg = AudioSegment.silent(duration=5000)

chunks = split_on_silence(seg, min_silence_len=1000, silence_thresh=-16)
```

Running this raises an exception instead of returning. I'd expect a fully-silent input to just produce no chunks (there's nothing non-silent to split out, after all) rather than crash — that way I can keep iterating over the rest of my files without having to special-case "is this clip silent?" before every call.
