# Mode: Greenfield

A new project with no code yet, or code so early that its choices are still open.

## Entry signals
- "I'm building / starting a new …", "which stack should I use for …"
- No repository yet, or only a scaffold.

## Evidence first
- If there's a scaffold, read it: what has already been chosen (language, framework, tooling)?
- Read `memory/preferences.md` for familiar technologies. That's a team-skill criterion only.
- When candidate technologies come up, load their `knowledge/` files and fetch current docs (latest stable versions, support/LTS windows).

## Required facts (stop rule)
You may recommend once you know:
1. **Purpose:** what problem it solves, for whom.
2. **Users and scale:** number of users, expected growth, traffic pattern.
3. **Clients:** web, mobile, CLI, API-only, and whether it must work offline.
4. **Data:** what's stored, how it relates, consistency needs, retention.
5. **Constraints:** deadline, budget, required cloud or vendor, compliance.
6. **Team:** who builds and runs it, and what they know.
7. **Operations:** who's on call, deployment target, expected lifespan (prototype or long-lived).

## Question bank
- What's the one thing this must do well? (decides the main criterion)
- Who uses it: just you, a team, or the public? (decides auth, scale, multi-tenancy)
- Web, mobile, or both? Does mobile need offline? (decides client stack and sync)
- Is the data relational (users → lists → tasks) or document-shaped? (decides the database)
- Is there a required cloud, or a budget limit per month? (decides hosting)
- Who maintains it in a year? (decides how much complexity is acceptable)
- Is this a prototype to throw away, or a product? (decides how much rigor)

## Challenging the user's choices
Only after the requirements are known. Challenge each choice against a specific requirement. "You said X. Is that the best fit for requirement R, given evidence E?" A choice that fits the requirements and the team needs no challenge. Say it fits, and why.

## Analysis focus
- One-way doors first: language/runtime, primary database, hosting model, auth model, data model.
- Separate decisions: the frontend framework and the backend language are usually independent.
- Operating cost and complexity count as much as development speed.

## Output
- **ADR** for each one-way-door decision (stack, database, hosting).
- **Plan** for the initial project skeleton: structure, first milestones, human setup steps (accounts, cloud projects).
