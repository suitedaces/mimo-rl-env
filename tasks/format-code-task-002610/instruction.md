Project-specific requirements
Would be nice to have an ability to specify project-specific requirements, so that if requirements are specified for a project then this settings overrides the global requirements file.

This feature would be very useful for developing page objects, when these're located in a separate project from Scrapy project.

The config may look like:

```yml
stacks:
  default: "scrapy:2.8"

projects:
  prod: 123456  # global requirements.txt used
  dev:
    id: 654321
    requirements:
      file: requirements-dev.txt  # project-specific requirements used

requirements:
  file: requirements.txt
```
