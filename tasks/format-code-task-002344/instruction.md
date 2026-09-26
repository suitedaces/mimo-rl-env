CLI option to disable installing dependencies
Right now, if you want to bootstrap a new project using `npx projen`, you can either use the `--no-synth` flag to just generate the `.projenrc.js` file, or you can generate all of the files and install all of the associated dependencies. There is no in between option.

It would be nice to be able to just generate the project-related files without also automatically running `yarn install` etc. to make it easier to test projen. I wanted to create a snapshot test which records a list of all of the files that are generated for the different project types, but this test ended up taking 4+ minutes on my local machine due to the time it takes to install dependencies of each project using yarn. If I remove the `postSynthesize()` part of `NodeProject` which installs all of the dependencies, then the test only takes a few seconds to run.

----

A couple implementation options that come to mind:
- make a general CLI flag called `post-synthesis` that disables the `postSynthesis` step
- extend `Project` to have a general `installDependencies` method that can be overwritten, refactor `NodeProject` to use it, and create a general CLI flag called `install-deps` that determines if this method gets called
- add an option to `NodeProject` called `installDeps` that specifically disables installing npm modules (this will automatically add an associated CLI flag)
