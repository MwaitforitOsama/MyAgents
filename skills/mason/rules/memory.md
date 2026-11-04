# Memory rules

Mason's memory lives in this skill's `memory/` folder. It is in git, so it follows the user to every device and every harness.

## Files

| File | Holds |
|---|---|
| `memory/preferences.md` | How the user likes to work: communication style, output format, depth |
| `memory/learnings.md` | Lessons that apply across projects, each with its evidence label and source, e.g. "`npm run dev` in project X also ran migrations. Read scripts before running them [run]" |

## What does NOT go in memory

- **Project decisions.** These go in that project's `docs/adr/`.
- **Secrets,** credentials, tokens, internal hostnames or customer data.
- **Facts about this one conversation** that won't matter next time.
- **Anything already in the project repo.**

## Reading

Read both files at the start of every session. They are **context, not requirements**:
- A preference like "prefers table-driven tests" shapes how you write code. It never overrides the plan or the project's existing conventions.
- If memory conflicts with what the user says now, the user wins. Offer to update the memory.

## Writing

- Save something when the user states a lasting preference, or when you learn something that will matter in other projects.
- Tell the user in one line what you saved. Every entry is dated: `- 2026-10-31: <entry>`.
- Update or remove entries that are wrong or outdated. Don't keep duplicates.
- Keep entries short: one line each.
