### Description

# Summary

As a developer, I want a workable way of dismissing the HMR overlay with a screen reader.

# Problem

When there is an error or warning in my project and the HMR overlay appears, I cannot dismiss the dialog.

# Reason

I am using a screen reader. I cannot "click outside" as the dialog suggests.


### Suggested solution

# Proposed Solution

One or all of these.

- Add "dismiss" button so that I can press the button and close the dialog
- Allow the escape key to dismiss the dialog



### Alternative

`server.hmr.overlay = false` exists, but this is not a perfect solution because:

- It cannot be applied for collaborating projects because it affects everyone else
- the difficulty for dismissing the dialog itself is the root of the problem, and avoiding it just by a hack is not ideal



### Additional context

# Notes

I am using vite in one of the projects as a collaborator. Vite version is 4.1.1. Sorry if the problem is already solved in newer versions.


### Validations

- [X] Follow our [Code of Conduct](https://github.com/vitejs/vite/blob/main/CODE_OF_CONDUCT.md)
- [X] Read the [Contributing Guidelines](https://github.com/vitejs/vite/blob/main/CONTRIBUTING.md).
- [X] Read the [docs](https://vitejs.dev/guide).
- [X] Check that there isn't already an issue that request the same feature to avoid creating a duplicate.
