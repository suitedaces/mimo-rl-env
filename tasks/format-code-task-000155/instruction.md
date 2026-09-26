[Bug] 0920 (unused-variable) false positive with nested for loops
### What happened?

0920 has a false positive that is somehow related to nested for loops. Commenting out the inner loop in the below code results in no unused variables reported. 5.3.0 doesn't report it with the inner loop so this is probably related to #1093 / #1104

### What command/code did you try to run?

sample.resource:
```robotframework
*** Keywords ***
Do Stuff With Events
    [Arguments]    ${initial_token}
    ...    ${retries}=5
    # don't want to mutate the original
    VAR    ${continuation_token}    ${initial_token}

    FOR    ${i}    IN RANGE    ${{ int($retries)+1 }}
        ${response} =    Get Events    ${continuation_token}
        FOR    ${_}    IN    @{response}[events]
            # Do stuff
            No Operation
        END

        IF    $i < int($retries)
            VAR    ${continuation_token}    ${response}[continuationToken]
        END
    END


Get Events
    [Arguments]    ${token}
    RETURN    ${{ {'continuationToken': int($token) + 1, 'events': []} }}
```
and then run `robocop sample.resource`

### What is the full error message?

`sample.resource:15:20 [I] 0920 Variable '${continuation_token}' is assigned but not used (unused-variable)`

### What did you expect to happen instead?

No unused variables reported

### Operating System

Ubuntu 24.04

### Robocop version

5.4.0, 5.5.0, 5.6.0
