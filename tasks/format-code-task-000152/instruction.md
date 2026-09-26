Rule could-be-keyword-tags: Ignore some builtin tags
`could-be-keyword-tags` highlights situations where all keywords in a file use the same tag. These tags can be consolidated in the Settings section instead.

In my code base, it keeps raising situations where all keywords use `robot:flatten` or `robot:private`. These tags are instructions for the Robot Framework runtime. Because of this, I don't think they should be consolidated like other tags. I want to keep them explicit.

Potential fixes:

1. Keep it the way it is.
2. Always ignore `robot:*` tags ([full list](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#reserved-tags))
3. Add a configurable parameter to this rule that allows users to exclude specific tags.
