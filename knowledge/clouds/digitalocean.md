# DigitalOcean

## Detect
`doctl` in scripts, `.do/app.yaml` (App Platform spec), Terraform `digitalocean` provider, `registry.digitalocean.com` image paths.

## Resource structure and access
- **Teams → Projects → resources.** Projects group resources for organization; access is managed at team level. Check the docs for current role options.
- **API tokens:** personal access tokens used by `doctl` and Terraform. Check the docs for token scopes and expiry options, and use the narrowest available.
- Reference: https://docs.digitalocean.com/platform/

## Service map (verify current names and features in docs)
| Need | Services to evaluate |
|---|---|
| Containers / compute | App Platform, Droplets, Kubernetes (DOKS) |
| Functions | Functions |
| Managed databases | Managed Databases (check docs for current engines: PostgreSQL, MySQL, MongoDB, caching, Kafka, OpenSearch…) |
| Object / block storage | Spaces (S3-compatible), Volumes |
| Networking | VPC, Load Balancers, Cloud Firewalls, DNS, Reserved IPs |
| Images | Container Registry |
| Observability | Monitoring, Uptime |

## Official sources
- Docs home: https://docs.digitalocean.com
- doctl reference: https://docs.digitalocean.com/reference/doctl/
- API reference: https://docs.digitalocean.com/reference/api/
- Pricing: https://www.digitalocean.com/pricing
- Status: https://status.digitalocean.com
- Console: https://cloud.digitalocean.com

## Read-only inspection (guard-allowed)
```
doctl account get
doctl projects list
doctl apps list
doctl apps get <app-id>
doctl compute droplet list
doctl kubernetes cluster list
doctl databases list
doctl compute firewall list
```
Never `doctl kubernetes cluster kubeconfig …`, `doctl databases connection …` or `doctl databases user …`. They reveal credentials, and the guard blocks them.

## Decision checkpoints
- App Platform (managed, less control) vs DOKS (Kubernetes, more ops) vs Droplets (full control, most ops).
- Managed DB vs self-hosted on Droplets: backups, failover, maintenance windows.
- Private networking (VPC) between apps and databases; trusted sources on managed DBs.
- Bandwidth/egress allowances and overage pricing (pricing page).
- Region availability of the services you need.
- Growth path: what happens if you outgrow a service (limits in the docs).

## Implementation (Mason)
- Prefer changing infrastructure as code (`.do/app.yaml`, Terraform) over console or CLI changes, so it's reviewable.
- Anything that creates, changes or deletes cloud resources, or deploys, goes to the user first, every time. The Mason guard forces a prompt for these commands.
- Read-only `doctl ... list/get` is fine for checking state.
