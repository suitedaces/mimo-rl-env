github releases support generating release notes using a parameter sent on release creation, see here:
https://docs.github.com/en/rest/reference/repos#create-a-release--parameters (parameter name is `generate_release_notes`).

supporting this feature will simplify release notes generation for github based repos.

(I'd expect this to be exposed as a new github plugin option, something like `autoGenerate`.)
