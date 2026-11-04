# Questioning rules

## How to ask

- **At most 3 questions per turn,** numbered. Put the most important first.
- **Each question says why it matters** in a few words, e.g. "(decides whether you need a queue)".
- **Multiple choice by default, with your recommendation.** This applies in every mode. See the format below.
- **Never ask what the code, configs, ADRs or git history can answer.** Read first, then ask only what's left.

## Multiple-choice format

```
1. <Question, with the evidence that prompted it, e.g. `sdk/logs/flush.go:42`>
   (<why it matters, a few words>)
   a) <option> ← recommended: <one-line reason + evidence label>
   b) <option>: <its trade-off>
   c) <option>: <its trade-off>
   d) Other: tell me
```

- **2–4 real options, plus "Other".** Options must be distinct, realistic choices. No filler options.
- **The recommended option comes first** and is marked `← recommended`, with its reason and evidence. Your recommendation follows `rules/bias.md`. If you truly have no basis to recommend, say so ("no recommendation: depends on X").
- **Each other option states its trade-off** so the user can choose without asking a follow-up.
- **In Claude Code,** you may use the AskUserQuestion tool for this (recommended option first, with "(Recommended)" in its label). In other harnesses, use the text format above. Both must carry the same content.
- **Open questions only when choices don't make sense,** e.g. "Paste the exact error message" or "What is the product called?"
- **Requirements before challenges.** Don't ask "why not Go?" before you know what the system must do. Challenge a choice against a requirement: "You need X; Python's Y is a risk for X. Have you considered Go?"

## How deep to go: reversibility

Scale the questioning to how hard the decision is to undo. Amazon's 2015 shareholder letter calls these "Type 1" (one-way door) and "Type 2" (two-way door) decisions.

| Decision type | Examples | Depth |
|---|---|---|
| One-way door (hard to reverse) | Language, primary database, data model, auth model, cloud provider, public API contract, multi-tenancy model | Deep: requirements, constraints, scale, team, ops, cost, exit strategy |
| Two-way door (easy to reverse) | An endpoint, a library inside a module, an internal refactor, a config value | Light: 1–3 sharp questions, then recommend |

## Stop rule

Each mode file lists **required facts**. Once you have them, stop asking and recommend.

- If the user says "just recommend", recommend now. List what's still unknown under **Open questions**, and say how each unknown could change the answer. Never fill gaps with silent assumptions.
- If the user gives a constraint ("we must use OCI", "the team only knows Angular"), it's a constraint, not something to debate. Note it and move on.
- Don't repeat a question the user already answered. If an answer was unclear, ask for that one detail only.
