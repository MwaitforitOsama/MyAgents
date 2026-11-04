# MongoDB

## Detect and version
- Drivers: `go.mongodb.org/mongo-driver`, `mongodb`, `mongoose`; `mongodb://` / `mongodb+srv://` URLs; `mongo:<tag>` images
- Version: `mongosh <uri> --quiet --eval "db.version()"`, the image tag, or the managed service console/CLI

## Official sources
- Manual: https://www.mongodb.com/docs/manual/
- Release notes: https://www.mongodb.com/docs/manual/release-notes/
- Driver docs: https://www.mongodb.com/docs/drivers/
- Data modeling: https://www.mongodb.com/docs/manual/data-modeling/
- Mongoose (if used): https://mongoosejs.com/docs/

## Decision checkpoints
- **Fit:** is the data document-shaped (read together, few cross-entity joins) or relational? Compare honestly with Postgres when it's a one-way-door decision.
- **Embedding vs referencing,** and document growth over time.
- **Indexes** that match real queries; compound index order.
- **Transactions:** whether multi-document transactions are needed, and the deployment requirements for them (check the docs).
- **Schema validation** at the DB level vs only in the app.
- **Scaling:** replica sets, sharding and shard key choice (one-way door).
- **Hosting:** managed (Atlas or a cloud's managed offering) vs self-hosted.

## Checks
- `db.<coll>.getIndexes()` and `.explain("executionStats")` on slow queries.
- Unbounded arrays inside documents.
- Read/write concern settings match the consistency needs.
- No `$where` or server-side JS on user input.
