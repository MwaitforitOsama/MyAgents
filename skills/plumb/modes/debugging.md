# Mode: Debugging

Find the **root cause** of a problem. Don't propose fixes until the cause is confirmed. That's Bugfix mode.

## Entry signals
- "Why does X happen", "it's slow / failing / flaky / crashing", "I can't figure out why…"
- Configuration that "doesn't work", e.g. "Traefik middleware isn't applied".

## Evidence first
1. **Symptoms exactly:** error messages, logs, status codes, timings. Ask for them if not available. Never guess them.
   - If there is a Jira ticket, read it first. If there is a Fullstory session, review it for console errors, failed requests and the user's last steps. Follow `rules/tickets-and-sessions.md`.
2. **Reproduce it** if you can: run the failing test, start the app and `curl` it, or take a headless screenshot.
3. **Read the code path** from entry point to failure.
4. **Check what changed:** `git log` / `git diff` around when it started.
5. **Read the config** involved, plus the version-matched docs for that tool. For example, read the Traefik docs for the exact version before explaining middleware behavior.
6. **Runtime state if relevant:** `docker compose logs`, `kubectl describe`, `kubectl logs`, cloud read-only `list/describe`.

## Required facts (stop rule)
1. Exact symptom and how to reproduce it (or why it can't be reproduced).
2. Expected vs actual behavior.
3. Environment: local, staging or prod, plus versions.
4. When it started, and what changed around then.
5. The root cause **confirmed by evidence**: a reproduction, log line or code path. Not just plausible.

## Method
1. List **hypotheses**, each with the evidence for and against it.
2. For each, name the **cheapest check** that would confirm or rule it out.
3. Run the checks (or ask the user to run what you can't), and update the hypotheses.
4. Stop when **one hypothesis explains every symptom** and the others are ruled out.

Label each hypothesis's status: `confirmed`, `ruled out`, or `open`.

## Question bank
- What exactly do you see: the error, the log line, the status code? (no guessing symptoms)
- Did this ever work? What changed since? (narrows the search)
- Does it happen everywhere, or only in one environment or for some users? (narrows scope)
- Can you share the output of `<specific command>`? (when you can't run it yourself)

## Output
- A **root cause summary** in chat: cause, evidence, and why the other hypotheses were ruled out.
- Then offer to **switch to Bugfix mode** to plan the fix. A plan is written only in Bugfix mode.
- If the cause stays unknown, write a short **plan** of the next diagnostic steps (Human steps / Agent steps) so work can continue.
