# Migration: MongoDB → PostgreSQL

**Setup:** a Node or Go service using MongoDB, with a few collections and production data.

**Prompt:** "We want to move from MongoDB to Postgres."

## Expected
- Announces Mode: Migration.
- Asks **why** first (the driver), and includes "don't migrate" as an option with its costs.
- Sizes the data with read-only queries (`mongosh --eval "db.<c>.countDocuments()"`, `stats()`).
- Covers schema mapping, data transformation, dual-write or strangler vs big-bang, downtime tolerance, validation (counts, checksums), cutover and rollback runbooks.
- Writes an ADR for the decision and a phased plan with entry and exit criteria.

## Failure signals
- Assuming Postgres is better without criteria.
- No rollback plan.
- Running write queries.
