Please answer these questions before submitting a bug report.

### What version of godog are you using?
Godog version is: v0.10.0

### What version of Go are you using?
go version go1.14.7 linux/amd64

### What did you do?
If possible, provide a recipe for reproducing the error.
I added a new features/foo.feature to my project and ran `godog .` for the first time in that project.

### What did you expect to see?
godog suggesting the new framework functions listed at `// godog v0.10.0 (latest)` in the README.md with the correct regex for the steps. I just defined.
```
You can implement step definitions for undefined steps with these snippets:
[...]

func InitializeTestSuite(ctx *godog.TestSuiteContext) {
	ctx.BeforeSuite(func() { 
		// clean state for the first rune
	})
}

func InitializeScenario(ctx *godog.ScenarioContext) {
	ctx.BeforeScenario(func(*godog.Scenario) {
		// clean the state before every scenario
	})

	ctx.Step(`regex`, stepcall)
}
```
### What did you see instead?
example code for the deprecated calls
```
You can implement step definitions for undefined steps with these snippets:
[...]

func FeatureContext(s *godog.Suite) {
	s.Step(`regex`, stepcall)
}
```

### Additional context
I use a project with Go modules.
feature file at features/happydogs.feature
```gherkin
Feature: Happy dogs
  As a dog owner
  I want my dogs to be happy
  So that it will make me happy as well

  Scenario: Initially the dog is sad
    Given 2 dogs
    When they play with no balls
    Then they are still sad

  Scenario: If they have at least one ball they are happy
    Given there are 2 dogs
    When they play with 1 ball
    Then then all dogs will be happy
```
Full output of godog .
```plain
$ godog .
Feature: Happy dogs
  As a dog owner
  I want my dogs to be happy
  So that it will make me happy as well

  Scenario: Initially the dog is sad # features/happydogs.feature:6
    Given 2 dogs
    When they play with no balls
    Then they are still sad

  Scenario: If they have at least one ball they are happy # features/happydogs.feature:11
    Given there are 2 dogs
    When they play with 1 ball
    Then then all dogs will be happy

2 scenarios (2 undefined)
6 steps (6 undefined)
246.175µs

You can implement step definitions for undefined steps with these snippets:

func dogs(arg1 int) error {
	return godog.ErrPending
}

func thenAllDogsWillBeHappy() error {
	return godog.ErrPending
}

func thereAreDogs(arg1 int) error {
	return godog.ErrPending
}

func theyAreStillSad() error {
	return godog.ErrPending
}

func theyPlayWithBall(arg1 int) error {
	return godog.ErrPending
}

func theyPlayWithNoBalls() error {
	return godog.ErrPending
}

func FeatureContext(s *godog.Suite) {
	s.Step(`^(\d+) dogs$`, dogs)
	s.Step(`^then all dogs will be happy$`, thenAllDogsWillBeHappy)
	s.Step(`^there are (\d+) dogs$`, thereAreDogs)
	s.Step(`^they are still sad$`, theyAreStillSad)
	s.Step(`^they play with (\d+) ball$`, theyPlayWithBall)
	s.Step(`^they play with no balls$`, theyPlayWithNoBalls)
}
```
