# Problem Statement

I’m using `yo aspnet` to scaffold ASP.NET 5 web apps that I want to run in Docker, but I still have to hand-write the Dockerfile every time. Could the web templates include a basic Dockerfile by default, and maybe let me add one separately with something like a Dockerfile generator command?

# Expected outcomes

- **Dockerfile in web-style scaffolds**
  - When `yo aspnet` is used to generate ASP.NET 5 web-style project templates that support running the app, the generated project root includes a file named `Dockerfile`.
  - This should apply to the relevant web-oriented templates exposed by the generator, without requiring callers to run a separate Dockerfile step.

- **Standalone Dockerfile generator**
  - A standalone `yo aspnet:Dockerfile` command is available.
  - Running `yo aspnet:Dockerfile` in a target location creates a file named `Dockerfile` there.

- **Generated Dockerfile contents**
  - Any `Dockerfile` produced by the main web scaffolds or by `yo aspnet:Dockerfile` uses `microsoft/aspnet:1.0.0-beta7` as its base image.
  - It copies `project.json` into `/app/`, sets `/app` as the working directory, restores dependencies with `dnu restore`, copies the project into `/app`, exposes port `5000`, and starts the app with `dnx -p project.json kestrel`.

- **Standalone generator usage text**
  - The `aspnet:Dockerfile` generator has usage/help text describing that it creates a Docker configuration file.
  - The usage/help text shows the example command `yo aspnet:Dockerfile` and indicates that the created file is `Dockerfile`.

# Implementation notes

- The internal organization of templates, shared template files, helper methods, and copy logic is up to the implementation.
- The Dockerfile behavior should be consistent whether it is produced as part of a project scaffold or by the standalone generator.
- Keep the implementation compatible with the existing Yeoman generator conventions used by this repository.
