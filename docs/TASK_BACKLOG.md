# Executable phase task backlog

**Status notation:** `[ ]` = not verified, `[x]` = evidence verified. All checkboxes begin unchecked intentionally. Existing local POC smoke evidence is documented in [EXECUTION_ROADMAP.md](EXECUTION_ROADMAP.md), but cannot substitute for independent phase approval.

Each task includes owner **role**, dependency IDs, expected artifact/test evidence and concrete acceptance criterion. Task IDs remain stable even if scheduled weeks change. Create child GitHub issues or PRs referencing these IDs.

## Initiation — phases 01–04

- [ ] **FDE-001** (Sponsor/FDE, depends: none): Charter CTO goals, exclusions, budget and risk appetite. Evidence: `docs/engagement/CHARTER.md`; acceptance: dated sponsor signoff.
- [ ] **FDE-002** (FDE/Product Owner, depends: 001): Interview 5 stakeholder roles and map as-is/to-be workflows. Evidence: `docs/engagement/DISCOVERY.md`; acceptance: product owner validates 3 prioritized journeys and exceptions.
- [ ] **FDE-003** (FDE/Finance, depends: 002): Estimate human baseline, unit economics, 3-tier POC/pilot/prod forecast. Evidence: `docs/engagement/BASELINE.md`; acceptance: assumptions and denominators reviewable.
- [ ] **FDE-004** (Architect/Security, depends: 002): C4, ADRs, data flow, STRIDE, tenant isolation and threat mitigations. Evidence: `docs/architecture/`; acceptance: independent security/architecture decision recorded.
- [ ] **FDE-005** (Product Owner/QA, depends: 002,004): Map user stories to NFRs, test cases, SLOs and approvals. Evidence: updated `docs/TRACEABILITY.md`; acceptance: no unmapped critical requirement.

## Foundation and secure integration — phases 05–06

- [ ] **FDE-006** (Platform/QA, depends: 004): Clean-room clone/test/build/smoke on Git Bash and Linux; assert first ingestion then replay. Evidence: `docs/evidence/local/` with commit, versions, commands and logs; acceptance: both paths pass unattended.
- [ ] **FDE-007** (Platform/Security, depends: 006): Lock transitive Python dependencies, base image digest, SBOM, SAST, SCA and secret checks. Evidence: lock file and CI artifacts; acceptance: reproducible, scanned immutable build.
- [ ] **FDE-008** (Backend/Data, depends: 004,006): PostgreSQL schema, Alembic migrations, transactions, tenant RLS and seeded synthetic fixtures. Evidence: migrations and DB tests; acceptance: fresh start and replay produce same expected state, cross-tenant denied.
- [ ] **FDE-009** (Security/Backend, depends: 004,008): Real OIDC JWT validation, server-derived tenant/RBAC/ABAC and expired/revoked token handling. Evidence: identity integration/E2E negative tests; acceptance: spoofed headers and cross-tenant claims cannot authorize.
- [ ] **FDE-010** (Backend/Integration, depends: 008,009): Typed versioned ITSM/CRM adapters, verified webhook signatures, idempotency, retries, outbox/DLQ. Evidence: OpenAPI, pact/contract tests, failure replay logs; acceptance: duplicates, bad signatures and transient faults handled safely.

## Retrieval, agents and customer UI — phases 07–09

- [ ] **FDE-011** (Data/AI, depends: 008,009): Document ingestion, lineage, delete/re-index, access-aware hybrid retrieval and citations. Evidence: fixtures and retrieval tests; acceptance: no unauthorized chunks returned even under adversarial queries.
- [ ] **FDE-012** (AI/QA, depends: 011): Blind adjudicated eval set, baseline, abstention thresholds, cost/latency/quality measures, prompt injection suite. Evidence: versioned `evals/` and report; acceptance: sponsor-approved predeclared thresholds met or NO-GO documented.
- [ ] **FDE-013** (AI/Security, depends: 009,010,012): Stateful agent workflows with typed bounded tools, separate policy engine, approval TTL, replay protection, kill switch. Evidence: policy and E2E attack tests; acceptance: zero unauthorized real writes in test suite.
- [ ] **FDE-014** (Full-stack/QA, depends: 009,011,013): Analyst inbox, citation UX, human approval queue, manager SLA and audit dashboards. Evidence: browser E2E/accessibility tests; acceptance: role-specific journeys tested with no UI-only authorization.

## POC — phase 10

- [ ] **FDE-015** (FDE/QA, depends: 006,010,012,013,014): Reproducible demo script covering normal, denied, abstained, duplicate, outage and rollback journeys. Evidence: `docs/poc/POC_TEST_PLAN.md`, demo video/log IDs; acceptance: independent clean-room operator runs scripted demo.
- [ ] **FDE-016** (FDE/Product Owner, depends: 015): Compare workflow metrics with baseline and present POC risk/cost decision. Evidence: `docs/poc/POC_RESULTS.md`, `GO_NO_GO.md`; acceptance: sponsor + security signoff (G3).

## Staging and quality — phases 11–12

- [ ] **FDE-017** (Platform, depends: 007,009,010): Terraform AWS VPC/EKS/RDS/S3/SQS/KMS, dedicated staging tenant, IaC PR review. Evidence: `infra/terraform/`, approved plan; acceptance: rebuild from state and restore documented without manual console drift.
- [ ] **FDE-018** (Platform/SRE, depends: 017): Helm, Argo CD, GitOps immutable image promotion, secret distribution, rollback. Evidence: `infra/helm/`, `infra/argocd/`, promotion log; acceptance: rollback and reapply tested.
- [ ] **FDE-019** (QA/Security, depends: 012,013,018): End-to-end performance, load, injection, tenancy, supply-chain and outage tests. Evidence: `docs/evidence/staging/`; acceptance: no outstanding release-blocking finding; signoff documented.
- [ ] **FDE-020** (SRE/Platform, depends: 018): OpenTelemetry tracing, audit export, Prometheus/Grafana SLO dashboards, on-call alerts, verified backup restore. Evidence: screenshots as supplementary, machine-readable results as primary; acceptance: alert, rollback and restore drills pass.

## Pilot — phase 13

- [ ] **FDE-021** (Product Owner/FDE, depends: 016,019,020): Define approved cohort, data rights, scope, shadow mode and halt conditions. Evidence: `docs/pilot/PILOT_PROTOCOL.md`; acceptance: customer + security permit pilot.
- [ ] **FDE-022** (AI/QA/Customer SMEs, depends: 021): Run shadow mode with human-adjudicated comparison, segment performance and error review. Evidence: `PILOT_SCORECARD.md`, anonymized evaluation IDs; acceptance: quality/adoption/cost thresholds measured, not assumed.
- [ ] **FDE-023** (FDE/Security, depends: 022): Limited low-risk write enablement under approvals and feature flags; execute rollback rehearsal. Evidence: approval and audit report; acceptance: no out-of-policy action; G5 decision signed.

## Production readiness — phase 14

- [ ] **FDE-024** (SRE/Security, depends: 019,020,023): Define negotiated SLO/error budget, RPO/RTO, runbooks, incident tree, pen-test closure and audit retention. Evidence: `docs/production/PRR_CHECKLIST.md`, DR test; acceptance: named owners sign G6.
- [ ] **FDE-025** (Release Owner, depends: 024): Assemble immutable artifact and release manifest with rollback/canary thresholds and change ticket. Evidence: `RELEASE_RECORD.md`; acceptance: change manager approves exact digest.

## Production and hypercare — phase 15

- [ ] **FDE-026** (SRE/FDE, depends: 025): GitOps deploy and staged canary with feature flag initially off, gradual approval-scoped writes, live telemetry. Evidence: `GO_LIVE_RUNBOOK.md`, `CANARY_REPORT.md`; acceptance: agreed guardrails and rollback criteria tested.
- [ ] **FDE-027** (SRE/Product Owner, depends: 026): Hypercare triage, KPI versus baseline, incident reconciliation, cost and SLO report. Evidence: `HYPERCARE_LOG.md`, `PRODUCTION_ACCEPTANCE.md`; acceptance: G7 customer acceptance and no unresolved critical risk.

## Handover — phase 16

- [ ] **FDE-028** (Customer Operations/SRE, depends: 027): Transfer architecture, access responsibilities, alerts, runbooks, DR plans and support ownership; run supervised incident drill. Evidence: `docs/handover/HANDOVER_CHECKLIST.md`, training record; acceptance: operator demonstrates routine and emergency operations.
- [ ] **FDE-029** (FDE/Product Owner, depends: 028): Final business impact report, productization backlog, lessons learned, technical defense. Evidence: `FINAL_BUSINESS_REPORT.md`, `INTERVIEW_DEFENSE.md`; acceptance: Sponsor and Operations Owner sign G8.

## Reproducibility exit rule (every task)

1. PR links the task ID, ADR/user story, threat where applicable, and exact commit SHA.
2. A reviewer can run commands from a fresh clone with documented platform, seed and configuration.
3. CI test links include unit, integration, security or evaluation results as appropriate.
4. All service dependencies and credentials come from declared configuration; synthetic data never contains customer secrets.
5. Rollback/reset and failure reproduction are documented; fixed seed or pinned dataset/model versions are recorded.
6. Only verified evidence closes the task; no green badge is substituted for independent review.
