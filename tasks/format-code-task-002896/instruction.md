Errors in writing the output configuration file are ignored
### 🐛 Bug Report

-   `tslint-to-eslint-config` version: 0.1.7
-   ESLint version: N/A
-   Node version: **8.X**

#### Actual Behavior

`npx tslint-to-eslint-config` prints out happy console messages but doesn't signal any error when creating an output `.eslintrc.js` file fails.

#### Expected Behavior

Logging the error and exiting with a non-zero status code would sure be nice!

There's a line something like `await dependencies.writeConfigurationFile(...);` where the result value is ignored. If that write method returns a failure result, that should be returned by `runCli` as a failure result.

#### Reproduction

```
mkdir temp
cd temp
npm init --yes
echo "{}" > tslint.json
npx tslint-to-eslint-config
```

~This will fail silently on **Node 8.X** because of #63. Note that #63 tracks fixing the Node 8 crash; this issue is for correctly logging any failure such as that one.~ Presumably, this issue will come up again if the writing of the configuration file fails for a permissions issue.
