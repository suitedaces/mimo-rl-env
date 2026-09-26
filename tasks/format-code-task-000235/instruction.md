<!-- If you don't know your Rasa NLU version, here is some help: https://goo.gl/g9QQg2. If you are creating a feature request, feel free to remove all the system information stuff. --> 

**Rasa NLU version**: 0.13.4

**Operating system** (windows, osx, ...): Windows

**Content of model configuration file**:
```yml
language: "en"

pipeline: "spacy_sklearn"
```

**Issue**:
The endpoint /evaluate of Rasa NLU HTTP server (server.py) is not up-to-date compared to the evaluate.py script of Rasa NLU. In particular it does not evaluate entities (only intents) and encounters some bugs that the script does not have.

Thus it would be great if Rasa NLU HTTP server could be inline with the latest evaluate.py script or maybe directly call it internally. Thanks!
