[Bug] argument-overwritten-before-usage is raise but there is no variable on the line.
### What happened?

launch robocop with the following configuration file:
```
--configure line-too-long:line_length:200                                                                                                               
--configure wrong-import-order:severity:error
--configure return_status:quality_gate:E=0:W=3:I=-1
--exclude too-many-arguments
--exclude too-long-keyword
--exclude file-too-long
--exclude missing-doc-test-case
--exclude too-long-test-case
--exclude too-many-calls-in-test-case
--exclude not-allowed-char-in-name
```

The following warning message is raised:
/opt/robotframework/tests/trustme-company-tests/auth/odif/odif.robot:95:21 [W] 0921 Keyword argument '${resp}' is overwritten before usage (argument-overwritten-before-usage)

But on line 95 there is no ${resp} variable there is only 83 line in the file:

```
*** Settings ***
Documentation       Auth / Odif non-regression tests

Library             Collections
Library             RequestsLibrary
Library             FakerLibrary
Resource            ${PATH_KEYWORDS}/device.resource
Resource            ${PATH_KEYWORDS}/encoder.resource
Resource            ${PATH_KEYWORDS}/signature.resource
Resource            ${PATH_KEYWORDS}/simulator.resource
Resource            ${PATH_KEYWORDS}/user.resource
Resource            ${PATH_KEYWORDS}/auth.resource

Test Tags           auth  odif  no-regression


*** Test Cases ***
AP-88-ODIF-01 Positive Scenario: Create Odif Challenge
    ${device}=              Create A Random Device  # robocop: disable=unused-variable
    ${resp}=                Create An Odif Challenge  device=${device}
    Dictionary Should Contain Key  ${resp}          value
    Dictionary Should Contain Key  ${resp}          blob

AP-88-ODIF-02 Positive Scenario: Create An Odif Authentication Method Without Header
    ${device}               ${user}=                Enroll A New Random User  authentication_method=odif  device_validation=${TRUE}
    ${m}=                   Get User Authentication Methods  user=${user}   device=${device}
    List Should Contain Value  ${m}                 fingerprint_local

AP-88-ODIF-03 Delete an odif authentication method
    Given A User With Odif And Password Authentication Method
    When I Delete The Odif Authentication Method
    Then The Fingerprint Local Method Should Be Removed
    And The User Should Not Use Odif Method To Verify


*** Keywords ***
Add A Password Authentication On The User Created
    [Documentation]  Add a password authentication method to a user
    ...    A user with ${USER} should be created in setup
    ${password}=    Create A Password
    ${resp}=    Create A Password Authentication Method     ${password}
    Status Should Be    201     ${resp}

Get User Authentication Methods
    [Documentation]  Query user info to get the associated authentication
    ...    methods.
    [Arguments]     ${user}=${user}     ${device}=${device}
    ${resp}=    Get My User     user=${user}    device=${device}
    Dictionary Should Contain Key   ${resp}     authentication_methods
    RETURN  ${resp}[authentication_methods]

A User With Odif And Password Authentication Method
    [Documentation]  Signup a user with odif and password
    ${device}   ${user}=    Enroll A New Random User    authentication_method=odif  device_validation=${TRUE}
    Verify Odif Using Attribute Name    user_id     user=${user}    device=${device}    http_code=200

    ${m}=   Get User Authentication Methods     user=${user}    device=${device}
    List Should Contain Value   ${m}    fingerprint_local
    List Should Contain Value   ${m}    password
    Set Test Variable   ${DEVICE}
    Set Test Variable   ${USER}

I Delete The Odif Authentication Method
    [Documentation]  Delete odif authentication method

    ${payload}=     Create Dictionary   user_id=${USER}[id]     device_id=${DEVICE}[id]     method=fingerPrintLocal

    ${headers}=     Create Dictionary   Authorization=Bearer ${USER}[jwt]

    Delete On Trustme   ${payload}  ${headers}  /auth/odif  device=${DEVICE}    expected_status=204

The ${authentication_method} Method Should Be Removed
    [Documentation]  Check method remove and password still available

    ${m}=   Get User Authentication Methods
    List Should Not Contain Value   ${m}    ${authentication_method}
    List Should Contain Value   ${m}    password

The User Should Not Use Odif Method To Verify
    [Documentation]  Check that verify method with odif
    ...    Should not be available

    Verify Odif Using Attribute Name    user_id     http_code=401
```



### What command/code did you try to run?

robocop -A configurationfile.txt

### What is the full error message?

/opt/robotframework/tests/trustme-company-tests/auth/odif/odif.robot:95:21 [W] 0921 Keyword argument '${resp}' is overwritten before usage (argument-overwritten-before-usage)

### What did you expect to happen instead?

no message or the right indication.

### Operating System

linux

### Robocop version

4.0.1
