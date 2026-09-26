## Sonar analysis crashes on surefire reports produced by JUnit 5.2

We recently upgraded one of our Java projects from JUnit 4 to JUnit 5.2 and started running our usual SonarQube analysis (with the sonar-java plugin) on the build. As soon as the surefire test reports are picked up by sonar, the analysis blows up and exits — the run never completes.

If we delete the surefire XML reports before running sonar, or revert the test framework back to the previous JUnit version, the analysis goes through fine, so the trigger really seems to be the report files that JUnit 5.2 generates with the surefire plugin. The exact same project + same sonar version was working before the JUnit upgrade.

It looks like sonar-java doesn't expect something about the shape of these reports. From a user point of view this is pretty disruptive — JUnit 5.2 + surefire is a fairly standard combo and it shouldn't take the whole analysis down. Could sonar-java be made resilient to whatever JUnit 5.2 is putting into these reports, so the analysis keeps running instead of crashing?
