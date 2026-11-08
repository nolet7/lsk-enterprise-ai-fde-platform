# Product versus demo: production go/no-go gates

The reference POC is not production-ready. Its security is intentionally minimal so local reproduction is possible without a customer IdP. Every row below is a hard gate for a real deployment.

| Gate | Required verified evidence | Current |
|---|---|---|
| Identity | OIDC with signature, issuer, audience, expiry and tenant-claim verification | NOT DONE |
| Authorization | RBAC/ABAC, immutable tenant binding, DB RLS or stronger isolation | NOT DONE |
| Action control | Policy engine, approval expiry, idempotent connectors, outbox | NOT DONE |
| AI quality | real model, grounded citations, blind evaluation and adversarial tests | NOT DONE |
| Data security | encryption, key management, approved retention, DLP and egress | NOT DONE |
| Cloud infrastructure | peer-reviewed Terraform, secure EKS and private routing | NOT DONE |
| Software supply chain | hashed dependency lock, signed artifacts, SBOM, scanners | NOT DONE |
| Observability | SLO dashboards, trace correlation and safe alerting | NOT DONE |
| Operational resilience | tested rollback, RTO/RPO and restored backups | NOT DONE |
| Business | accepted pilot metrics, cost model and customer sponsor signoff | NOT DONE |
| Governance | threat model, security authorization and ongoing owner | NOT DONE |

## Work sequencing

Foundation -> verified data contracts -> secure tenant identity -> RAG access control -> agent/action policy -> UI -> POC measurement -> EKS staging -> performance/security/AI evaluations -> shadow pilot -> operational readiness -> gradual production -> handover.

## Explicit prohibitions

- Do not deploy the local demo API to a public IP or accept real customer PII.
- Do not connect a model-produced tool call to write-capable real integrations until a policy gate exists.
- Do not publish a numeric quality claim based only on synthetic or proxy labels.
- Do not treat a deployment, green CI check or generated diagram as formal production acceptance.
