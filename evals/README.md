# Mr. Plumb and Mason evals

Scenarios that check Mr. Plumb's and Mason's behavior is the same across models. Behavior means mode, process, evidence, neutrality and output format. Run them whenever you change the skill, and whenever you try a new model (Claude, GPT via Codex, Gemini, local via Ollama).

## How to run (manual for now)

1. Open a fresh session as the agent the scenario names (`claude --agent plumb -n plumb`, `claude --agent mason -n mason`, or both in separate terminals for `mason-*` scenarios).
2. Set up what the scenario's **Setup** says (a sample repo, or none).
3. Send the **Prompt** exactly as written. Follow up as the scenario describes.
4. Score each **Expected** line pass/fail, and note any **Failure signals** you saw.
5. Record the result in the table below.

A scenario passes only if every Expected line passes and no Failure signal appears.

## Results log

| Date | Model | Harness | Scenario | Pass/Fail | Notes |
|---|---|---|---|---|---|
| | | | | | |

## Scenarios

| File | Tests |
|---|---|
| `greenfield-python-todo.md` | Requirements before challenging a stack choice |
| `feature-go-delete.md` | Reads existing code; no language questions; feature-level questions |
| `debugging-root-cause.md` | Hypotheses + evidence; no fix before the cause is confirmed |
| `bugfix-known-cause.md` | Regression test, blast radius, rollback |
| `refactoring-scope.md` | "Leave it" as an option; tests before restructure |
| `migration-mongo-postgres.md` | Data, cutover, rollback, dual-run |
| `nextjs-version-sensitive.md` | Detects version and router before advising |
| `cloud-oci-manual-steps.md` | Manual step format, docs-based console paths, secrets |
| `cloud-unknown-provider.md` | Research procedure + draft knowledge file |
| `bias-option-order.md` | Same recommendation regardless of option order |
| `bias-pushback-no-new-info.md` | Doesn't cave without new information |
| `bias-leading-question.md` | Neutral answer to a leading question |
| `decision-override.md` | Challenge once, accept, record concerns |
| `evidence-no-docs.md` | Says "unverified" when docs can't be fetched |
| `review-branch.md` | Thorough branch review: callers, DRY, leaks, structure, copy-ready comments, no checkout |
| `questions-multiple-choice.md` | Multiple-choice questions with a recommendation, in any mode |
| `mason-dispute-flawed-plan.md` | Mason checks the plan against the code, disputes with evidence, user decides |
| `mason-run-request.md` | Plumb's blocked command reaches the user through Mason, in every mode |
| `mason-review-loop.md` | Review findings go back only with the user's yes; 3-round cap; no auto-commit |
| `mason-standalone.md` | Mason without Plumb: small task flow vs recommending a plan |
| `mason-freedom-in-chat.md` | Chat can't change permissions; high-impact commands always prompt |

The guard hooks have their own automated tests: `python3 claude/hooks/tests/run_guard_tests.py` (Plumb) and `python3 claude/hooks/tests/run_mason_tests.py` (Mason).
