## `del self.options.fPIC` fails when `shared` is set from the command line

I have a pretty standard recipe that follows the shared/fPIC pattern that's all over the conan docs:

```python
class Pkg(ConanFile):
    name = "pkg"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
```

If I just run `conan install .` everything works fine — `shared` defaults to `False`, the `if` is false, nothing gets removed.

But the moment I try to build the shared variant from the command line:

```
conan install . -o pkg*:shared=True --build=missing
```

it blows up with:

```
ConanException: Incorrect attempt to remove option 'fPIC' with current value 'True'
```

It looks like as soon as `shared` has been given a value from outside the recipe, `del self.options.fPIC` is no longer allowed — even though removing fPIC *based on* the shared value is exactly the documented pattern and the whole reason this `configure()` body exists. The conditional removal is the only way to express "fPIC doesn't make sense when shared=True", and it has to happen in `configure()`, which runs after the command-line / profile options have been applied.

I'd expect `del self.options.fPIC` inside `configure()` to just work in this case, regardless of whether `shared` got its value from `default_options` or from `-o`.
