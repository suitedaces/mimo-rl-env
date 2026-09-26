## Feature request: allow `manifest-update` to set the `<uses-sdk>` attributes

The `manifest-update` goal currently lets me drive a number of `AndroidManifest.xml` attributes from the POM (versionName, versionCode, sharedUserId, debuggable, supports-screens, compatible-screens, provider authorities, …), but I can't find any way to make it touch the `<uses-sdk>` tag.

My use case is fairly standard: I have several Maven profiles producing different APK flavors, and depending on the profile I'd like to write a different `android:minSdkVersion` / `android:targetSdkVersion` (and occasionally `android:maxSdkVersion`) into the generated manifest, instead of having to keep multiple checked-in `AndroidManifest.xml` files or pre-process the file with another plugin.

What I'd like to be able to write inside the existing `<manifest>` configuration block of the `manifest-update` goal is something along these lines:

```xml
<plugin>
  <groupId>com.jayway.maven.plugins.android.generation2</groupId>
  <artifactId>android-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>update-manifest</id>
      <goals><goal>manifest-update</goal></goals>
      <configuration>
        <manifest>
          <versionName>1.2.3</versionName>
          <versionCode>123</versionCode>
          <!-- new: drive <uses-sdk> from the POM -->
          <uses-sdk>
            <minSdkVersion>14</minSdkVersion>
            <targetSdkVersion>21</targetSdkVersion>
          </uses-sdk>
        </manifest>
      </configuration>
    </execution>
  </executions>
</plugin>
```

After running `manifest-update`, the resulting `AndroidManifest.xml` should contain a `<uses-sdk>` element whose `android:minSdkVersion`, `android:maxSdkVersion` and `android:targetSdkVersion` reflect whatever I configured (and only the ones I configured — anything I leave out shouldn't be forced into the manifest). All three attributes should be configurable; in profile-based builds it's pretty common to want to bump just `targetSdkVersion` while leaving the rest alone.

It would be nice if this followed the same conventions as the other manifest-update knobs (i.e. settable via the `<manifest>` block as shown above, and also reachable as a top-level mojo parameter so it can be set from `pom.xml` properties / command line in the same style as the existing ones).
