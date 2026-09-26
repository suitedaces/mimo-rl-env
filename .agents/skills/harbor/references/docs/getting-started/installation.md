> ## Documentation Index
> Fetch the complete documentation index at: https://docs.harborframework.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Installation

> Install Harbor.

## Install Harbor

Install Harbor with a Python package manager.

<Tabs>
  <Tab title="uv">
    First, [install uv](https://docs.astral.sh/uv/getting-started/installation/).

    ```bash theme={"system"}
    uv tool install harbor
    ```
  </Tab>

  <Tab title="pip">
    ```bash theme={"system"}
    pip install harbor
    ```
  </Tab>

  <Tab title="uv upgrade">
    ```bash theme={"system"}
    uv tool uninstall harbor
    uv tool install harbor
    ```
  </Tab>
</Tabs>

## Nightly builds (not frequently used for most users)

We publish [a dev release](https://pypi.org/project/harbor/#history) from the latest `main` to [PyPI](https://pypi.org/project/harbor/) daily. Install it with a pre-release flag (stable installs are unaffected):

<Tabs>
  <Tab title="uv">
    ```bash theme={"system"}
    uv tool install --prerelease explicit 'harbor>=0.dev0'
    ```
  </Tab>

  <Tab title="pip">
    ```bash theme={"system"}
    pip install --pre harbor
    ```
  </Tab>

  <Tab title="uv upgrade">
    ```bash theme={"system"}
    uv tool uninstall harbor
    uv tool install --prerelease explicit 'harbor>=0.dev0'
    ```
  </Tab>
</Tabs>

## Configure a sandbox

Harbor runs agents in sandboxes. By default, Harbor uses [Docker](https://www.docker.com/) as the sandbox runtime, so you'll need to [have Docker installed](https://docs.docker.com/get-started/get-docker/) on your machine.

However, many users find it more productive to use a cloud sandbox. See [Pre-integrated sandboxes](/core-concepts/sandboxes/pre-integrated-sandboxes) for a list of out-of-the-box cloud sandbox options.

For non-Docker sandboxes, you'll need to install the extra dependencies. E.g.

<Tabs>
  <Tab title="uv">
    ```bash theme={"system"}
    uv tool install "harbor[modal]"
    ```
  </Tab>

  <Tab title="pip">
    ```bash theme={"system"}
    pip install "harbor[modal]"
    ```
  </Tab>
</Tabs>
