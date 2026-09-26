### New Issue Checklist

- [x] Updated fastlane to the latest version
- [x] I read the [Contribution Guidelines](https://github.com/fastlane/fastlane/blob/master/CONTRIBUTING.md)

### Issue Description

The Apple Vision Pro launches this Friday and I'm trying to ship our visionOS app to TestFlight, but `fastlane pilot upload` rejects `xros` as a platform.

When I run something like:

```
bundle exec fastlane pilot upload \
  --api-key-path <REDACTED> \
  --team_id <REDACTED> \
  --app_platform xros \
  --ipa ./MyVisionApp.ipa
```

pilot bails out complaining that the platform can only be `ios`, `appletvos`, or `osx`. If I leave `--app_platform` off, it eventually prompts me for the platform and only offers those same three values, so there's no way to tell pilot the build is for visionOS.

The ipa itself is a perfectly valid visionOS build — App Store Connect accepts it when uploaded via Xcode / Transporter directly — pilot is the only thing in my pipeline that refuses it.

Could `xros` be added as a recognized platform for pilot alongside `ios`, `appletvos`, and `osx`? Right now Vision Pro releases through fastlane are fully blocked on this.

### Environment

- fastlane pilot
- target platform: visionOS (xros)
