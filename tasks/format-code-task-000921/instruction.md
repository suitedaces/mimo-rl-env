Bug: Select when passed a value as Prop errors with a suggestion to pass readOnly
Seems weird when we try to use a `select` component, and pass a value as a prop, it prompts with the error to either set `onChange` or `readOnly`.
the `readOnly` at the last seems misleading since the `select` component does not have a `readOnly` prop, unlike inputs which do  have a `readOnly` attribute.

**SELECT PROPS**
https://react.dev/reference/react-dom/components/select

seems an easy fix would be to check if the mounted component is a `select` component and then conditionally just change the error message, though would need to add tests to support the same.

https://github.com/facebook/react/assets/72331432/12674152-7d57-4d98-99e6-635577b31bfe

cc @sophiebits 

codesandbox link to tinker:- https://codesandbox.io/s/admiring-wright-9sctsn?file=/src/App.js
