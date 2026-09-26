Problem Statement

I keep copying the same base HPC Container Maker recipe bits into multiple recipes, like the Ubuntu/GNU compiler setup, and it’s getting annoying to keep them in sync. I’d like to be able to include another recipe file from a recipe, preferably by a relative path next to the main recipe, so its Stage0/Stage1 additions show up in the generated Dockerfile/Singularity output.

Expected Outcomes

- Recipe authors can include another recipe file from within a recipe through the public `hpccm.include(recipe_file)` API.
- Included recipe files execute as part of the same recipe-building process, so additions they make to recipe state, including Stage0 and Stage1 content, building blocks, primitives, and values needed later by the including recipe, are reflected in the final generated container specification.
- Relative include paths are resolved relative to the recipe being processed rather than the caller’s current working directory; absolute include paths continue to work as absolute paths.
- Include failures are handled consistently with recipe loading: by default, file-open or execution errors are logged and terminate with exit code 1, while calling `hpccm.include(..., raise_exceptions=True)` propagates the underlying exception.
- The examples should demonstrate reusing a sibling recipe file to avoid duplicating common development-environment setup.

Implementation Notes

- Preserve existing recipe execution behavior and output generation for recipes that do not use includes.
- The internal mechanism for locating, executing, and sharing recipe state is up to the implementation, as long as the public behavior above is satisfied.
- The implementation should work for both Dockerfile and Singularity generation paths supported by the existing recipe workflow.
