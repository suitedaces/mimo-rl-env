### `cmake_find_package_multi` doesn't honor the kebab-case lowercase config file naming

According to the CMake docs for [`find_package` Config Mode](https://cmake.org/cmake/help/latest/command/find_package.html#config-mode-search-procedure), CMake recognizes two naming conventions for the package config files:

```
<PackageName>Config.cmake
<lowercase-package-name>-config.cmake
```

…and similarly for the version file (`<PackageName>ConfigVersion.cmake` / `<lowercase-package-name>-config-version.cmake`).

In my recipes I've been setting a lowercase filename for the multi generator, e.g.

```python
def package_info(self):
    self.cpp_info.filenames["cmake_find_package_multi"] = "mylib"
    # ...
```

because downstream I want to do `find_package(mylib CONFIG REQUIRED)` and follow the lowercase-with-dash style that CMake documents. But after `conan install` the only files I see in the generators folder are:

```
mylibConfig.cmake
mylibConfigVersion.cmake
mylibTargets.cmake
mylibTarget-release.cmake
```

I'd expect that when the filename I'm asking for is all lowercase, the generator produces the `mylib-config.cmake` / `mylib-config-version.cmake` form instead, since that's the convention CMake associates with lowercase package names. When the filename has uppercase characters (e.g. `MyLib`) the current `MyLibConfig.cmake` style is fine and shouldn't change.

Could `cmake_find_package_multi` be taught to pick the right naming style based on the case of the filename?
