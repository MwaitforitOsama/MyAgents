# Oracle Cloud Infrastructure (OCI)

## Detect
`ocid1.` identifiers, `~/.oci/config`, the `oci` CLI in scripts, Terraform `oci` provider, `*.ocir.io` image paths.

## Resource hierarchy and access
- **Tenancy** (the root compartment) → **Compartments** (nestable) → resources. Compartments are the main unit of isolation and access control.
- **Regions → Availability Domains → Fault Domains.** Check the docs for how many ADs the target region has.
- **Identity Domains:** users, groups, dynamic groups (for instance/resource principals), applications.
- **Policies** are statements in OCI's policy language, attached to a compartment, e.g. `Allow group <group> to <verb> <resource-type> in compartment <name>`. Verbs: `inspect`, `read`, `use`, `manage`. Reference: https://docs.oracle.com/en-us/iaas/Content/Identity/home.htm
- **Workloads:** prefer instance/resource principals with dynamic groups over API keys on servers. Check the identity docs for current guidance.

## Service map (verify current names and features in docs)
| Need | Services to evaluate |
|---|---|
| Containers / compute | Compute (VM/bare metal), Container Engine for Kubernetes (OKE), Container Instances |
| Functions | OCI Functions |
| Relational DB | Autonomous Database, OCI Database with PostgreSQL, MySQL HeatWave, Base Database |
| NoSQL | OCI NoSQL Database |
| Object / block / file storage | Object Storage, Block Volume, File Storage |
| Networking | VCN, subnets, security lists / NSGs, Load Balancer, Network Load Balancer, DNS, API Gateway |
| Secrets / keys | Vault (keys and secrets) |
| Messaging | Streaming, Queue, Notifications |
| Images / CI | Container Registry (OCIR), DevOps |
| Observability | Logging, Monitoring, APM |

## Official sources
- Docs home: https://docs.oracle.com/en-us/iaas/Content/home.htm
- CLI reference: https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/
- Architecture Center: https://docs.oracle.com/solutions/
- Pricing / price list: https://www.oracle.com/cloud/price-list/
- Free tier (Always Free): https://www.oracle.com/cloud/free/
- Status: https://ocistatus.oraclecloud.com
- Console: https://cloud.oracle.com

## Read-only inspection (guard-allowed)
```
oci iam compartment list --compartment-id <tenancy-ocid> --all
oci iam policy list --compartment-id <compartment-ocid>
oci compute instance list --compartment-id <compartment-ocid>
oci ce cluster list --compartment-id <compartment-ocid>
oci network vcn list --compartment-id <compartment-ocid>
oci db autonomous-database list --compartment-id <compartment-ocid>
```
Never `oci secrets secret-bundle get` (it reveals secret values; the guard blocks it).

## Decision checkpoints
- Compartment design: per environment, per team, per application?
- Policies: least privilege, written per compartment, reviewed with `oci iam policy list`.
- Networking: public vs private subnets, NSGs vs security lists, NAT/service gateways.
- Always Free vs paid limits (check the free tier page; limits change).
- Managed DB choice vs self-managed on Compute.
- Console navigation changes often. For manual steps, always fetch current docs (`rules/manual-steps.md`).

## Implementation (Mason)
- Prefer changing infrastructure as code (Terraform `oci` provider, Resource Manager stacks) over console or CLI changes, so it's reviewable.
- Anything that creates, changes or deletes resources, or deploys, goes to the user first, every time. The Mason guard forces a prompt for these commands.
- Read-only `oci ... list/get` is fine for checking state. Never read secret bundles.
