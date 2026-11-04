# Google Cloud (GCP)

## Detect
`gcloud` in scripts or docs, `cloudbuild.yaml`, `app.yaml`, Terraform `google` / `google-beta` providers, `*.run.app` URLs, `*-docker.pkg.dev` / `gcr.io` image paths.

## Resource hierarchy and access
- **Hierarchy:** Organization → Folders → Projects → resources. Policies are inherited downward. Reference: https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy
- **IAM:** principals (users, groups, service accounts), roles (basic, predefined, custom), bindings on resources. Reference: https://cloud.google.com/iam/docs/overview
- **Workloads:** service accounts per workload, least privilege, avoid long-lived keys. Check the IAM docs for current best practices on keys and workload identity.

## Service map (verify current names and features in docs)
| Need | Services to evaluate |
|---|---|
| Containers / compute | Cloud Run, GKE, Compute Engine |
| Functions | Cloud Run functions (check current naming in docs) |
| Relational DB | Cloud SQL (Postgres/MySQL), AlloyDB, Spanner |
| Document / NoSQL | Firestore, Bigtable |
| Cache | Memorystore |
| Object storage | Cloud Storage |
| Messaging / jobs | Pub/Sub, Cloud Tasks, Cloud Scheduler |
| Networking | VPC, Cloud Load Balancing, Cloud DNS, Cloud CDN, Cloud NAT |
| Secrets / keys | Secret Manager, Cloud KMS |
| Images / CI | Artifact Registry, Cloud Build |
| Observability | Cloud Logging, Cloud Monitoring, Cloud Trace |

## Official sources
- Docs home: https://cloud.google.com/docs
- gcloud reference: https://cloud.google.com/sdk/gcloud/reference
- Architecture Framework: https://cloud.google.com/architecture/framework
- Pricing: https://cloud.google.com/pricing · Calculator: https://cloud.google.com/products/calculator
- Free tier: https://cloud.google.com/free
- Status: https://status.cloud.google.com
- Console: https://console.cloud.google.com

## Read-only inspection (guard-allowed)
```
gcloud config list
gcloud projects list
gcloud run services list --region <region>
gcloud run services describe <svc> --region <region>
gcloud sql instances list
gcloud compute instances list
gcloud projects get-iam-policy <project>
gcloud logging read "<filter>" --limit 50
```

## Decision checkpoints
- Project per environment (dev/staging/prod)? Folder structure?
- Serverless (Cloud Run) vs Kubernetes (GKE) vs VMs, based on traffic pattern, ops capacity and cost.
- Managed DB choice and its connectivity (private IP, connectors, proxies).
- Egress and inter-region costs (pricing pages).
- Region choice: latency, data residency, service availability per region.
- Lock-in: which services have portable equivalents (containers, Postgres) vs proprietary APIs.
