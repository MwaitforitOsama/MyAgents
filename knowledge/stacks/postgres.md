# PostgreSQL

## Detect and version
- Drivers: `pgx`, `lib/pq` (Go); `pg`, `postgres` (Node); ORMs with a postgres provider; `postgres://` URLs; `postgres:<tag>` images; migration folders
- Version: `PGOPTIONS='-c default_transaction_read_only=on' psql ... -c "SELECT version()"`, the image tag, or the managed service's read-only `describe`

## Official sources
- Docs, current: https://www.postgresql.org/docs/current/ (version-specific: replace `current` with the major, e.g. `/docs/16/`)
- Versioning and support policy: https://www.postgresql.org/support/versioning/
- Release notes: https://www.postgresql.org/docs/release/
- Wiki (community, rank 5): https://wiki.postgresql.org

## Decision checkpoints
- **Schema:** normalization, constraints (FK, unique, check), types, JSONB vs columns.
- **Indexes:** matching the real query patterns; partial and composite indexes.
- **Migrations:** tool, locking behavior of each change, zero-downtime patterns.
- **Connections:** pool size per app instance × number of instances vs `max_connections`; whether a pooler is needed.
- **Multi-tenancy:** shared tables with tenant column, row-level security, schema per tenant, or DB per tenant.
- **Backups and recovery:** PITR, restore testing, managed service guarantees.
- **Soft vs hard delete,** auditing, retention.

## Checks
- `\d+ <table>`: indexes on foreign keys that are used in joins/filters.
- `EXPLAIN (ANALYZE, BUFFERS)` on slow queries (read-only session; it executes the query).
- Long-running transactions and lock waits (`pg_stat_activity`, `pg_locks`, read-only).
- Migration statements that take strong locks on large tables (check the `ALTER TABLE` docs for lock levels).
- Version is within the community support window (versioning page) or the managed provider's.
