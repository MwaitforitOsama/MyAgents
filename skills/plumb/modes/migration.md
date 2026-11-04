# Mode: Migration

Moving data, a framework version, a database, infrastructure or a cloud provider. Examples: MongoDB → Postgres, an Angular major upgrade, REST → gRPC, DigitalOcean → OCI, Pages Router → App Router.

Migrations differ from refactoring: they carry **data risk and operational risk**, and need cutover and rollback plans.

## Entry signals
- "Move from X to Y", "upgrade to vN", "switch to …", "replace X with Y".

## Evidence first
1. **Current state:** versions, usage of the thing being migrated (`grep` for imports and APIs), data volume, deployment setup.
2. **Target state:** official migration guides and release notes for the exact source and target versions. Breaking changes, deprecations, required intermediate versions.
3. **Dependencies:** which libraries block the move (`npm ls`, `go list -m all`, and their compatibility notes).
4. **Data:** schemas, data size, write rate. Read-only queries are fine to size it.
5. **Runtime:** read-only cloud and cluster state for infra migrations.
6. **ADRs** that explain the current choice.

## Required facts (stop rule)
1. **Why migrate:** the concrete driver (end of support, cost, a limitation), with evidence.
2. **Scope:** what moves and what stays.
3. **Data:** volume, transformation needed, consistency needs during the move.
4. **Downtime tolerance:** zero, a maintenance window, or flexible.
5. **Rollback:** how far back you can go, and until when.
6. **Constraints:** deadline (e.g. end-of-support date), budget, team capacity.

## Question bank
- What forces this migration now? (is it needed, and how urgent)
- How much downtime is acceptable? (big-bang vs gradual)
- Can old and new run side by side for a while? (dual-run, strangler pattern)
- What's the point of no return, and how do you roll back before it? (risk)
- How will you prove the new system matches the old? (validation)

## Options to consider
- **Don't migrate / postpone**, with the cost of staying.
- **Big-bang cutover** in a maintenance window.
- **Gradual:** dual-write, strangler pattern, step-by-step version upgrades.

## Analysis focus
- Step-by-step version paths when skipping major versions isn't supported. Check the official upgrade guide.
- Data validation: counts, checksums, sampled comparisons.
- Cutover runbook and rollback runbook.
- Monitoring during and after.

## Output
- **ADR** for the decision to migrate and the chosen strategy.
- **Plan** with phases. Each phase has entry and exit criteria, rollback steps, data validation, and Human steps for console/infra work.
