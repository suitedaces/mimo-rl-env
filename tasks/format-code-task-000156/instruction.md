[Bug] import variable files with module name and arguments gives a wrong variables-import-with-args message
### What happened?

starting with this simple suite

```robot
*** Settings ***
Variables       variables    ${ENVIRON}

*** Variables ***
${ENVIRON}    dev

*** Test Cases ***
first test case
    Log    ${ENVIRONMENT_NAME}
```

where I import a variable file with arguments, I get this error:

```
...\import_vars.robot:2:1 [E] 0404 Robot and YAML variable files do not take arguments (variables-import-with-args)
```



### What command/code did you try to run?

robocop .\tests\import_vars.robot

### What is the full error message?

```
...\import_vars.robot:2:1 [E] 0404 Robot and YAML variable files do not take arguments (variables-import-with-args)
```

### What did you expect to happen instead?


starting from robotframework 5 it is possible to import variables with its module name like libraries, see also [documentation](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#taking-variable-files-into-use) 

so this message is invalid with robotframework version >= 5

I think the rule 0404 should check that the file extension is `yaml` and not `py`.
And are you shure that you can import `robot` files as variables? I think not. What do you mean with robot files?


### Operating System

windows, linux

### Robocop version

3.1.1
