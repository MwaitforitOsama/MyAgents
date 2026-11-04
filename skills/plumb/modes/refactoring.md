# Mode: Refactoring

Change the internal structure of code **without changing its external behavior**. This follows Martin Fowler's definition (refactoring.com). If behavior, data or infrastructure changes, it's Feature or Migration mode.

## Entry signals
- "Clean up", "split this", "decouple", "too messy", "make it testable", "extract a service/module".

## Evidence first
1. Read the code to refactor and everything that depends on it (`grep` for usages).
2. Measure the pain with evidence: file and function size, duplication, dependency tangles, change frequency (`git log --format= --name-only | sort | uniq -c | sort -rn | head`).
3. Check test coverage of the area. Run the tests. Refactoring without tests is a risk to name.
4. Read ADRs that explain why the code is shaped this way.

## Required facts (stop rule)
1. **The pain:** what concretely hurts (bugs, slow changes, onboarding, testability), with evidence.
2. **The goal:** what "better" means, measurably if possible.
3. **The safety net:** existing tests, or tests to add first.
4. **Scope and timebox:** what's in, what's out.
5. **Constraints:** parallel feature work, release timing.

## Question bank
- What change were you trying to make when this code got in the way? (real pain vs aesthetics)
- What does done look like? (scope)
- Is anyone else changing this code right now? (merge conflicts, sequencing)
- Can we ship in small steps, or does it have to land at once? (risk)

## Options to consider
Always include **"leave it as is"** as an option. Refactoring has a cost, and stable code that rarely changes may not be worth it. Compare incremental steps against a larger restructure.

## Analysis focus
- Small, behavior-preserving steps, each one releasable.
- Tests before structure changes.
- Keep public interfaces stable, or plan their deprecation.

## Output
- **Plan**: ordered small steps, each with "tests pass" as the acceptance criterion; characterization tests to add first; what stays untouched.
- **ADR** if the refactoring changes architecture (module boundaries, layering, service split).
