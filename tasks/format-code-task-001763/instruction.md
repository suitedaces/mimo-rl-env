Crash when using the "record audio" feature in the iOS pre-release
### Operating system

iOS

### Joplin version

13.3.1

### Desktop version info

Joplin Mobile 13.3.1 (prod, ios)

Client ID: d3e66a0d32b54e6bb895613e67349ff3
Sync Version: 3
Profile Version: 47
Keychain Supported: No

Revision: 200d3c84e (dev)

Extra Markdown editor settings: 1.10.1

iOS version: 18.3.1
FTS enabled: 1
Hermes enabled: 1

### Current behaviour

I'm getting an error when trying to use the voice recording feature in the latest iOS pre-release:
```
02-19T21:27:08: AudioRecording: Error starting recording: TypeError: undefined is not a function
TypeError: undefined is not a function
    at formatMsToDurationLocal (/Users/laurent/Library/Developer/Xcode/DerivedData/Joplin-ewsyxzklwwggmtdeyavpfmrkhqhv/Build/Intermediates.noindex/ArchiveIntermediates/Joplin/BuildProductsPath/Release-iphoneos/main.jsbundle:394609:26)
    at AudioRecordingBanner (/Users/laurent/Library/Developer/Xcode/DerivedData/Joplin-ewsyxzklwwggmtdeyavpfmrkhqhv/Build/Intermediates.noindex/ArchiveIntermediates/Joplin/BuildProductsPath/Release-iphoneos/main.jsbundle:586516:87)
```

For context, `formatMsToDurationLocal` is a new function that was added to `@joplin/utils` when adding the audio recorder. It's used for displaying the recording duration.

Here are a few possible causes of the issue:
- `@joplin/utils` wasn't rebuilt with the latest changes before the iOS release was created.
- There's an issue with the duration formatting logic.

### Expected behaviour

Joplin should not crash when attempting to record audio.

### Logs

_No response_
