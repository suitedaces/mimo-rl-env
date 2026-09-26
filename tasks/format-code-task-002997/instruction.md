I want the `werf config graph` CLI command to print the image dependency graph from the rendered `werf.yaml` configuration.

The command should be invoked as `werf config graph [IMAGE_NAME...] [options]`. With a config that defines `app1` depending on `baseImage`, `app2` depending on `baseImage` and importing `app1`, and `baseImage` with no dependencies, running `werf config graph` should exit 0 and print this YAML shape on stdout:

```yaml
- image: app1
  dependsOn:
    from: baseImage
- image: app2
  dependsOn:
    from: baseImage
    import:
    - app1
- image: baseImage
```

When I pass a specific image name, such as `werf config graph app2`, the command should exit 0 and print only that image's graph entry in the same YAML format. The command should support `--final-images-only` so only final selected images are included. A selector that matches no images, such as `werf config graph missing-image`, should return a non-zero exit code and write the selection error to stderr. `werf config graph --help` should exit 0 and show the syntax `werf config graph [IMAGE_NAME...] [options]` together with the description that it prints the dependency graph for images in `werf.yaml`.
