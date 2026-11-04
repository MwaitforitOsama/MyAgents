# Refactoring: "clean up this handler file"

**Setup:** a project with one large handler file (500+ lines) and modest test coverage.

**Prompt:** "This handlers file is a mess. Help me refactor it."

## Expected
- Announces Mode: Refactoring.
- Measures the problem with evidence: size, duplication, change frequency from git history.
- Asks what change the mess is blocking (real pain vs aesthetics).
- Includes "leave it as is" as a serious option.
- Requires tests before restructuring. Proposes characterization tests if coverage is weak.
- Plan has small, behavior-preserving steps, each ending with "tests pass".

## Failure signals
- A big-bang rewrite plan with no tests first.
- Changing behavior as part of the refactor.
