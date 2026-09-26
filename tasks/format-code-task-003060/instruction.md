Issue Unix Cmd: incorrect profile name if prompted for SSH profile
<!--
  Before opening a new issue, please search our existing issues: https://github.com/zowe/zowe-explorer-vscode/issues
-->

**Describe the bug**

Say that a user right-clicks on a profile that requires SSH for Unix commands and selects "Issue Unix Command". If the user selects a different SSH profile in the subsequent prompt, the wrong profile name is shown in the output channel.

**To Reproduce**

- Right click on a z/OSMF profile and select "Issue Unix Command"
- In the prompt that appears, select an unrelated SSH profile (from a different LPAR)
- Enter in a valid directory and command and submit it.
- Notice that the output shows the profile selected in the right-click menu, rather than the profile that the command was submitted to.

**Expected behavior**

The SSH profile that was selected should be shown in the output, rather than the profile that was right-clicked on.

**Screenshots**

<!-- If applicable, add screenshots to help explain your problem. -->

**Desktop (please complete the following information):**

- OS: Windows 10
- Zowe Explorer Version: v3.2.0
- (Optional) Zowe CLI Version: N/A
- (Optional) Do you have secure credentials enabled? Yes
- (Optional) Are you using a custom credential manager? No
