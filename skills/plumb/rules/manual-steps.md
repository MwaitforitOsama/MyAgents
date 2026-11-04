# Manual steps

When the user has to do something by hand (cloud consoles, dashboards, account settings, DNS, certificates, CLI setup), give step-by-step instructions in this exact format.

## Format

```markdown
### Step N: <short action title>
**Where:**  <exact location: Console → Menu → Section → Page, or the terminal and directory>
**Do:**     <the exact clicks, fields and values, or the exact command>
**Copy:**   <what to copy or download, and exactly where to put it>   (omit if nothing)
**Secure:** <how to protect any secret: file location, permissions, .gitignore, never paste in chat>   (omit if no secret)
**Verify:** <how the user can confirm this step worked, and what they should see>
**Source:** <official doc URL · checked YYYY-MM-DD>
```

## Rules

1. **One action per step.** If the user would need to scroll a page or switch apps mid-step, split it.
2. **Every step has a Verify line.** The user should know it worked before moving on.
3. **Console paths come from docs, not memory.** Cloud consoles change their navigation often. Fetch the official docs for the current UI. If you can't confirm a menu path, say "the menu location may differ, look for `<name>`" rather than guessing.
4. **Secrets:**
   - Tell the user where to store them (e.g. `~/.oci/`, a secret manager, a `.env` that's in `.gitignore`).
   - Give the permission command if relevant (e.g. `chmod 600 <file>`).
   - Tell them to check that `.gitignore` covers the file.
   - Never ask them to paste a secret into the chat.
5. **Exact values.** Field names, button labels and commands appear exactly as shown in the UI or docs, in `code` formatting.
6. **Prerequisites first.** Step 0 lists what the user needs beforehand: accounts, permissions or roles, installed CLIs with versions.
7. **End with a final check**, e.g. a command that proves the whole setup works.
8. **Placement.** In plans, these steps go under **Human steps**, never under **Agent steps**.
