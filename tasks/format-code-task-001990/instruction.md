## `web-ext run -t firefox-android` can't launch Firefox Nightly (`org.mozilla.fenix.debug`)

I'm trying to use `web-ext run` to test my extension against Firefox Nightly for Android, whose package id is `org.mozilla.fenix.debug` (this is the only Firefox-for-Android variant I have installed on the device).

Command I'm running:

```
web-ext run -t firefox-android \
  --adb-device <my-device-id> \
  --firefox-apk org.mozilla.fenix.debug
```

What happens:

- `web-ext` does detect the APK as a Firefox build — it shows up in the discovered Firefox APKs list and gets selected.
- But when it tries to actually launch the app on the device, Nightly never starts. The app just doesn't come up; the run fails before my extension is loaded.

If I install regular Firefox / Fenix release (`org.mozilla.fenix`) and point `--firefox-apk` at that one instead, everything works fine on the same device with the same command shape. So the launching pipeline itself is working — it just doesn't seem to handle the `org.mozilla.fenix.debug` variant correctly.

It would be great if `web-ext run -t firefox-android` could launch Firefox Nightly the same way it launches the other Firefox-for-Android builds. Nightly is what most extension developers are testing against day-to-day, so not being able to use it on Android via web-ext is pretty limiting.
