# System design and platform security review

## Current implementation

```
Local operator --> loopback-only FastAPI --> SQLite (disposable local file)
                         |                --> tenant-scoped audit
                         +--> deterministic keyword routing
                         +--> local-only mock approvals/actions
```

All identities and roles are provided through untrusted demo headers. This is a training POC and never safe on the public internet.

## Target production container architecture

```
Customer browser --> WAF/CDN --> ingress/ALB --> React app + FastAPI BFF
                                                |
                           Validated OIDC JWT / customer IdP + tenant RBAC/ABAC
                                                |
                      +-------------------------+-----------------------+
                      |                         |                       |
                 Ticket API                Knowledge API          Approval API
                      |                         |                       |
                 SQS / DLQ                 ingestion jobs          policy engine
                      |                         |                       |
                  ITSM/CRM                 S3 + pgvector          audited action bus
                                                |
                                      bounded RAG/agent runtime
                                                |
                                     Bedrock via private egress

Cross-cutting: EKS workload identity, KMS, network policies, OTEL, metrics,
logs (redacted), GitOps, IaC, SLOs, audit retention, recovery tests.
```

## Crucial architecture changes from the initial concept

1. Treat OIDC, data authorization and tenancy as **server-side trust boundaries**; never accept identity/tenant from user-controlled request headers in production.
2. Separate retrieval from action execution. Agent output is untrusted; a deterministic server-side policy engine authorizes each real tool operation.
3. Enforce access filters before retrieval, including document permission changes and index revocation. Require citations and abstention under weak or conflicting evidence.
4. Durable workflow state, queues, idempotent connectors and transactional outbox must precede production writes. Avoid ambiguous retry and double execution.
5. Production requires defined audit retention, PII redaction, encryption, key rotation, disaster recovery, documented failover and secrets lifecycle.
6. Separate customer product data, model providers, evaluation samples and telemetry; write down cross-border/subprocessor decisions.
7. Evaluate business outcomes against human and deterministic baselines; don't use proxy-label accuracy as a release gate.
8. Require final human approval for privileged operations; two-person control should bind to real immutable identities and expiration times.
9. CI supply-chain security requires pinned actions by immutable SHA, dependency and image scanning, SBOM, artifact signatures and promotion by digest.
10. Public infrastructure cannot be implied by a successful localhost demo; production rollout remains gated.

## Threat model — initial STRIDE scenarios

| Threat | Boundary | Minimum mitigation and evidence |
|---|---|---|
| Tenant crossing | API, vector search, logs | Verified token tenant claim + mandatory DB policies; negative E2E tests |
| Prompt injection | Documents / tools | Treat retrieved text as data; bounded tools; adversarial evals |
| Insecure direct object access | Ticket/action IDs | Scoped queries, policy checks, tampering tests |
| Unauthorized actions | Agent / tool adapter | Signed intent, server-side policy, least privilege, human approval |
| Replay / duplicate writes | Webhooks / queues | Authenticated webhook, idempotency key, dedupe window and transactional outbox |
| PII exfiltration | Model gateway / telemetry | DLP/PII policy, approved providers, token minimization, log redaction |
| Supply chain | Build & deploy | SAST, dependency scan, SBOM, signed digest, branch protection |
| Outage / resource exhaustion | EKS / model API | Rate limits, circuit breakers, queues, alerting, capacity tests |
| Approval spoofing | Human approvals | OIDC/step-up, separation of duties, approval expiry, audit |

## ADRs pending

- ADR-001 AWS EKS versus serverless (operational cost and team readiness)
- ADR-002 Bedrock versus customer-hosted models (region, privacy and cost)
- ADR-003 RDS pgvector versus dedicated vector service (scale, ACL consistency)
- ADR-004 Authentik federation versus direct customer IdP (ownership and compliance)
- ADR-005 Event sourcing versus transactional outbox (complexity and dedupe)
- ADR-006 Tenant isolation strategy (RLS, schema/database separation)

**None of these architectural options is approved simply by appearing here.**
