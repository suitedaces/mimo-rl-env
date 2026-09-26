bazel.Runfile fails to parse a MANIFEST file generated for rules_python
Full minimal reproduction repro with a running github action at: https://github.com/samhowes/rules_go_runfiles_repro
Failing github action run: https://github.com/samhowes/rules_go_runfiles_repro/runs/2370880759?check_suite_focus=true
Output of interest: `Error: panic: error parsing runfiles manifest: C:/users/runneradmin/_bazel_runneradmin/t32zp6hb/execroot/__main__/bazel-out/x64_windows-opt-exec-2B5CBBC6/bin/parent.exe.runfiles/MANIFEST:1: no space`

Sample manifest that reproduces this issue: https://github.com/samhowes/rules_go_runfiles_repro/blob/main/sample_MANIFEST

Target producing the output: `//:parent_output_test`

### What version of rules_go are you using?
1.16

### What version of gazelle are you using?

v0.23.0

### What version of Bazel are you using?

Build label: 4.0.0
Build target: bazel-out/x64_windows-opt/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer_deploy.jar
Build time: Thu Jan 21 07:39:16 2021 (1611214756)
Build timestamp: 1611214756
Build timestamp as int: 1611214756

### Does this issue reproduce with the latest releases of all the above?

The above are the latest releases

### What operating system and processor architecture are you using?

windows x64

### Any other potentially useful information about your toolchain?
its all standard

### What did you do?

I made a `py_binary` target that has a data dependency on a `go_binary` target then tried to execute the `go_binary` from within the `py_binary`. Inside of the `go_binary` I tried to execute ```path, err := bazel.Runfile("important.txt")``` to access a runfile that the `go_binary` has as a data dependency. 

On windows.

### What did you expect to see?

No err, and a successful location of the runfile.

### What did you see instead?

```error parsing runfiles manifest: C:/users/runneradmin/_bazel_runneradmin/t32zp6hb/execroot/__main__/bazel-out/x64_windows-opt-exec-2B5CBBC6/bin/parent.exe.runfiles/MANIFEST:1: no space```
