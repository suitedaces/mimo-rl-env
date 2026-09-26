## Problem Statement

我用 react-native-test-app 跑 RN 0.80 的项目，生成出来的 android/gradle/wrapper 里 Gradle 版本还是 8.11.1，结果 build 一直报兼容性问题。看了下 0.78、0.79 也是一样掉到老版本去了。能不能把这几个新 RN 版本对应的 Gradle wrapper 版本也支持上？

## Expected outcomes

- React Native 0.78、0.79、0.80 项目生成 Android Gradle wrapper 时，应使用各自兼容的较新 Gradle wrapper 版本，而不再回落到旧的 8.11.1 wrapper。
- 这些 React Native minor 版本下的 patch 版本也应得到一致处理，而不是只支持某个精确的 `.0` 版本号。
- Existing Gradle wrapper behavior for earlier supported React Native versions should remain unchanged.

## Implementation notes

- The exact implementation approach is up to you; choose whatever is consistent with the repository’s existing Android Gradle wrapper generation behavior.
- Preserve existing compatibility behavior outside the newly supported React Native version ranges.
