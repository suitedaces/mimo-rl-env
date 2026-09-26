Return `encoding` attribute from `info` for `sox_io` backend
The legacy sox backend exposed libsox's structures (`sox_signalinfo_t` and `sox_encodinginfo_t`) and that allowed to access most of audio metadata. In the transition to the new backends, these structures were abstracted away and we introduced `AudioMetaData` which only contain very basic information.  Now we would like to add some metadata, in this time, with more consistent behaviors across the backends.

We would like to add a `encoding` (string) attribute, which tells the encoding of audio data being inspected.

(See also #1173, #1094)

## Specifications

We will map the following libsox's [`sox_encoding_t` structure](https://fossies.org/dox/sox-14.4.2/sox_8h.html#ab0a659b0258d1989c751ba5415e6a4cd) to string type. The resulting string expression will be made available to user code via [`AudioMetaData` class](https://github.com/pytorch/audio/blob/99ed7183df3df8278cc46de432c31b254e31573e/torchaudio/backend/common.py#L6-L22)

torchaudio Representation | `sox_encoding_t` | PySoundFile subtype
-- | -- | --
`"PCM_S"` | SOX_ENCODING_SIGN2 | PCM_S8, PCM_16, PCM_24, PCM_32
`"PCM_U"` | SOX_ENCODING_UNSIGNED | PCM_U8
 `"PCM_F"` | SOX_ENCODING_FLOAT | FLOAT, DOUBLE
`"ULAW"` | SOX_ENCODING_ULAW | ULAW
`"ALAW"` | SOX_ENCODING_ALAW | ALAW
`"FLAC"` | SOX_ENCODING_FLAC | FLAC (format)
`"MP3"` | SOX_ENCODING_MP3 | 
`"VORBIS"` | SOX_ENCODING_VORBIS | VORBIS
`"AMR_WB"` | SOX_ENCODING_AMR_WB | 
`"AMR_NB"` | SOX_ENCODING_AMR_NB | 
`"OPUS"` | SOX_ENCODING_OPUS 
`"UNKNOWN"` | SOX_ENCODING_UNKNOWN or Others | Others


## Steps to implement

### sox_io backend
1. Implement the mapping
Add a function to perform the conversion from `sox_encoding_t` to `std::string` in [torchaudio/csrc/sox/io.cpp](https://github.com/pytorch/audio/blob/f1d8d1e0da44f6503c01ddcae2e40772b400ea2d/torchaudio/csrc/sox/io.cpp) before the [`get_info`](https://github.com/pytorch/audio/blob/99ed7183df3df8278cc46de432c31b254e31573e/torchaudio/csrc/sox/io.cpp#L39) function. (Put the implementation in anonymous namespace as it will only be used by `get_info` function).
2. Update `SignalInfo` class
Add `encoding` attribute and getter. [[interface](https://github.com/pytorch/audio/blob/f1d8d1e0da44f6503c01ddcae2e40772b400ea2d/torchaudio/csrc/sox/utils.h#L29-L44), [impl](https://github.com/pytorch/audio/blob/master/torchaudio/csrc/sox/utils.cpp#L64-L80)]
3. Update the [`get_info` function](https://github.com/pytorch/audio/blob/f1d8d1e0da44f6503c01ddcae2e40772b400ea2d/torchaudio/csrc/sox/io.cpp#L33-L50).
First retrieve the `sox_encoding_t` as `sf->encoding->encoding`, then pass it to the function defined above to get the string representation. Then return it via `SignalInfo` class.
4. Update the [`AudioMetaData`](https://github.com/pytorch/audio/blob/f1d8d1e0da44f6503c01ddcae2e40772b400ea2d/torchaudio/backend/common.py#L6-L19) class so that `format` attribute is accessible.
5. Update the Python Front end.
Update the [`info` function](https://github.com/pytorch/audio/blob/f1d8d1e0da44f6503c01ddcae2e40772b400ea2d/torchaudio/backend/sox_io_backend.py#L13-L35) so that the `format` attribute is passed to client code.

### soundfile backend
1. Implement mapping in `_soundfile_backend.py` and update [`info`](https://github.com/pytorch/audio/blob/41c76a17c7a191752eada5346dc88ecfe690dcae/torchaudio/backend/_soundfile_backend.py#L53-L79) function.
2. Update test

## Building and testing locally

The [`info_test.py`](https://github.com/pytorch/audio/blob/f1d8d1e0da44f6503c01ddcae2e40772b400ea2d/test/torchaudio_unittest/sox_io_backend/info_test.py) needs to be updated.

To work on this, `torchaudio` needs to be built from source. Use of `conda` environment (anaconda/miniconda) is highly recommended.

Also, build requires `cmake` and nightly build version of PyTorch. Refer to pytorch.org for the installation.
To install `cmake`, do `pip install cmake`.

Once the environment is setup, the following command will build and run the corresponding tests

```
BUILD_SOX=1 python setup.py develop
(cd test && pytest torchaudio_unittest -v -k "info_test"
```
