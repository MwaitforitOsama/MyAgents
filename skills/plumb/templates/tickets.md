# Tickets: <title>

- **Status:** Proposed | Approved | Sent to Mason | Creating | Done
- **Date:** YYYY-MM-DD
- **Jira site / project:** <site name> / <PROJECT KEY>  (checked with getVisibleJiraProjects)
- **Source:** <plan, ADR, review, audit report or conversation this comes from>

## Summary
<One or two sentences: why these tickets exist.>

## Duplicate check
<JQL you ran and what it found. List existing tickets that cover part of this, and say whether each is reused, linked or ignored.>

## Tickets

<One block per ticket. T-ids are local references used for links and parents below. Use only issue types and fields that getJiraIssueTypeMetaWithFields confirmed for this project; mark anything unchecked as unverified.>

### T1: <summary, as it will appear in Jira>
- **Issue type:** <Epic | Story | Task | Bug | Sub-task>  (checked)
- **Parent:** <none | T-id | existing key, e.g. ABC-12>
- **Priority:** <value, if the project has the field>
- **Labels:** <comma-separated, or none>
- **Components:** <or none>
- **Assignee:** <none, or a person the user named; never guess>
- **Description:**
  <Plain text Jira body: context, what to do, acceptance criteria. No secrets, no personal data from sessions.>

## Links
<Links to create after all tickets exist. Use link types from getIssueLinkTypes.>
- T2 **blocks** T3
- T1 **relates to** ABC-99

## Comments
<Comments on existing tickets, if any.>
- **ABC-99:** <comment text>

## Disputes
<Mason opens entries (D1, D2…) when something in this file doesn't hold against Jira; Plumb answers in the same entry. Format: rules/handoff.md, step 3.>

## Created (Mason fills this in)
| T-id | Key | Result |
|---|---|---|
| T1 | | |
