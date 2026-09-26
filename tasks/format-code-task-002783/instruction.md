Impossible to include base64 encoded imager in info.description section
<!--- Provide a general summary of the issue in the title above -->
<!--- 
  If you aren't sure what Swagger-UI version, see this guide: https://github.com/swagger-api/swagger-ui/blob/master/docs/usage/version-detection.md
--->

When trying to include base64 encoded images in API description, 
```<img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />```

the generated HTML seems to be sanitized:
```<img>```


| Q                               | A
| ------------------------------- | -------
| Bug or feature request?         |  Feature
| Which Swagger/OpenAPI version?  | 2.0
| Which Swagger-UI version?       | 3.x
| How did you install Swagger-UI? | /dist folder, on a webserver of my own
| Which browser & version?        | Chrome 64
| Which operating system?         | Windows 10


### Demonstration API definition
<!--- If you're describing a bug, please provide an API definition that reproduces your problem -->
<!--- If you have link to a demo repo please link that! -->

<!--- If your spec is large, please put it into a Gist (https://gist.github.com) instead of pasting it here. -->

```yaml
swagger: "2.0"
info:
  description: |
    This is a sample server Petstore server.  You can find out more about
    Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).
    For this sample, you can use the api key `special-key` to test the authorization
    filters.
    <img src="data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot" />
  
  version: "1.0.0"
  title: "Swagger Petstore"
  termsOfService: "http://swagger.io/terms/"
  contact:
    email: "apiteam@swagger.io"
  license:
    name: "Apache 2.0"
    url: "http://www.apache.org/licenses/LICENSE-2.0.html"
```

### Configuration (browser query string, constructor, config.yaml)
Default configuration

### Expected Behavior
The expected result is to have a red dot drawn in the description. 

### Current Behavior
Nothing is drawn, probably due to Sanitize and XSS risks (see issues #830, #3847 , etc..)

### Possible Solution
Can it be authorized without any injection risks? Can it be a setting?

### Context
<!--- How has this issue affected you? What are you trying to accomplish? -->
<!--- Providing context helps us come up with a solution that is most useful in the real world -->
For company internal policies and file distribution reasons, I would to add some pictures (team and company logo) inside the API description.

This can be done using a classical IMG html tag refering to an external file.

But I really need to keep the YAML file autonomous (for distribution reason).
