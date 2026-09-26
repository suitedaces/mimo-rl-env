userEvent.click(screen.getAll*) produces an ambiguous error
<!--
Thanks for your interest in the project. I appreciate bugs filed and PRs submitted!
Please make sure that you are familiar with and follow the Code of Conduct for
this project (found in the CODE_OF_CONDUCT.md file).

Please fill out this template with all the relevant information so we can
understand what's going on and fix the issue.

I'll probably ask you to submit the fix (after giving some direction). If you've
never done that before, that's great! Check this free short video tutorial to
learn how: https://kcd.im/pull-request


If this is an issue with the documentation, please file an issue in the docs repo:
https://github.com/testing-library/testing-library-docs

-->

- `@testing-library/dom` version: @testing-library/dom@7.29.4
- Testing Framework and version: Karma
  - karma@4.4.1
  - jasmine@3.3.1
- DOM Environment: Chrome Version 88.0.4324.182 (Official Build) (x86_64)

Relevant code or config

Repro sandbox: https://codesandbox.io/s/react-testing-library-demo-forked-u4lcu?file=/src/__tests__/hello.js

What you did:

I ran a test and tried to click the result of `screen.getAllByLabelText`. 

What happened:

Running the test produces something like:

![image](https://user-images.githubusercontent.com/841084/108136666-49657a00-706f-11eb-8a36-d117c527258d.png)

where the element in question is an array:

![image](https://user-images.githubusercontent.com/841084/108136688-5a15f000-706f-11eb-9853-1b404cd1d721.png)


Problem description:

The thrown error is a bit ambiguous -- there is room for improvement. 

Suggested solution:

I would assume that `userEvent` methods would error on having multiple elements -- where the error text would be a bit more direct. I am not sure if a user can interact with more than 1 element at a time.
