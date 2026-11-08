# FDE delivery execution roadmap — CTO mandate to handover

**Project:** LSK Enterprise AI Resolution Platform | **Customer:** fictional Meridian Financial Services | **Plan status:** proposed, tasks not automatically completed.

This roadmap is the operational source of truth for planned work. The existing [16-phase summary](DELIVERY_PLAN.md), [production gates](PRODUCTION_GATES.md), [reproducibility contract](REPRODUCIBILITY.md), and [traceability](TRACEABILITY.md) remain normative.

## Current verified baseline (2026-11-08)

- Commit `31a425f` corrected Docker host binding to `127.0.0.1:18000:8000`.
- Operator reported `docker compose ps`: container `Up (healthy)` and `API_URL=http://127.0.0.1:18000 python scripts/smoke.py`: `PASS smoke`, route `identity`, `idempotent_replay=True`.
- Existing replay output confirms detection of a previously ingested event; it **does not** demonstrate first-ingestion and replay in one clean test. Add a unique-event verification.
- Local deterministic POC only. No real OIDC, PostgreSQL, RAG, LLM, external write connector, AWS/EKS, production DR, or customer approval is implemented.
- Phase signoff is not inferred from passing tests. Every gate requires a named reviewer and dated evidence.

## Delivery control model

**Task states:** BACKLOG -> IN PROGRESS -> IN REVIEW -> VERIFIED (or BLOCKED). Only the reviewer marks VERIFIED against a linked evidence artifact. Retain failing test evidence and associated defect issue. No production work uses real customer data unless approved handling controls exist.

**Roles (fictional until assigned):** Sponsor/CTO (business funding), Customer Product Owner (workflow acceptance), FDE Lead (delivery), Platform Lead (infrastructure), Security Lead (security risk approval), AI Lead (evaluation), QA Lead (test acceptance), SRE Lead (operational go-live), Customer Operations Owner (handover). Implementer must not self-approve risk acceptance.

**Execution ordering:** See [TASK_BACKLOG.md](TASK_BACKLOG.md) for stable IDs, prerequisites, acceptance tests and evidence. The schedule below is illustrative, *not* a commitment. A blocker delays downstream gates.

| Track | Phases | Target weeks | Gate |
|---|---|---|---|
| Initiation and discovery | 01–03 | 1–2 | G0: signed scope and bounded POC authorization |
| Secure design and foundation | 04–06 | 2–5 | G1: architecture/security review and clean-room build |
| Knowledge, controlled agents and UX | 07–09 | 5–8 | G2: traceable functional and adversarial evaluation |
| POC demo and decision | 10 | 8 | G3: documented POC go/no-go |
| AWS staging and hardening | 11–12 | 8–11 | G4: staging, security and recovery tests pass |
| Pilot rollout | 13 | 11–13 | G5: pilot business AND risk approval |
| Production readiness | 14 | 13–14 | G6: signed production readiness review (PRR) |
| Controlled production / hypercare | 15 | 14–15 | G7: service acceptance after stable canary |
| Handover and closeout | 16 | 15–16 | G8: named owner accepts operations and artifacts |

## G0 — CTO mandate and customer discovery

**Tasks:** mandate / sponsor / boundaries; stakeholder RACI; structured interviews; as-is and to-be workflows; API, data and security constraints; sample data approvals; baseline methodology; POC budget and exit criteria. Keep requirements traceable to user stories, threats, tests and costs.

**Must produce:** `docs/engagement/CHARTER.md`, `STAKEHOLDERS.md`, `DISCOVERY.md`, `WORKFLOW_MAP.md`, `BASELINE.md`, `RISK_REGISTER.md`, `DECISION_LOG.md` (planned paths). Reviewer: Sponsor, Product Owner, Security Lead.

**Gate:** Signed, bounded POC scope; explicit prohibited actions/data; measurable success criteria. No signed evidence = G0 open.

## G1 — Secure architecture and engineering baseline

**Tasks:** C4 context/container/deployment diagrams; trust boundaries; data residency and retention; identity/tenant model; signed webhook strategy; request replay protection; policy decision points; DB tenant isolation; data contracts; CI scanning; dependency and image digests; deterministic seeded data; reproducible setup on a clean machine; rollback and failure modes.

**Must produce:** versioned ADRs, STRIDE threat assessment, data-flow diagram, OpenAPI contracts, setup script, evidence of clean-room Docker and Python validation, locked dependencies and CI outputs.

**Gate:** Architect + Security approve design, QA verifies fresh-clone setup. Demo header identity must remain strictly localhost-only until replaced.

## G2 — RAG, agents and authorized user experience

**Tasks:** authorized knowledge ingestion with lineage; deletion/reindex process; tenant ACL filtering before retrieval; hybrid search and citations; model-provider abstraction with timeout/cost controls; blind eval set and abstention; agent state machine; typed tools; policy evaluator; approval TTL and separation of duties; safe async retries; OIDC identity; role-aware UI; audit tracing.

**Must produce:** data fixtures, retrieval evaluation, model and prompt version registry, tool threat tests (prompt injection, malicious documents, unauthorized writes, tenant access), E2E UX and authorization reports.

**Gate:** AI + Security + Product Owner accept measured coverage, harmful-action prevention and user workflows. Do not claim model accuracy from synthetic-only labels.

## G3 — POC technical and business demonstration

**Tasks:** rehearse deterministic baseline vs AI-assisted workflow; show normal case, weak evidence, approval denial, API failure, duplicate event and tenant denial; collect timings with defined sample size; show costs, risks and unresolved defects; demonstrate reset/recreate locally.

**Must produce:** `docs/poc/POC_TEST_PLAN.md`, `POC_RESULTS.md`, `DEMO_SCRIPT.md`, `GO_NO_GO.md` with actual run IDs, denominators, limitations and sponsor decision.

**Gate:** G3 signed by Sponsor, Product Owner, Security Lead. POC passing does not authorize pilot writes.

## G4 — AWS staging, integration and resilience

**Tasks:** modular Terraform for networking, EKS, RDS, S3, queues, KMS and identities; VPC endpoints, network restrictions and tenancy controls; CI artifact provenance/SBOM/scan gates; GitOps with immutable images; secret manager; backup/restore; synthetic replay; service telemetry; alert rules; migration and rollback rehearsal; load and chaos testing.

**Must produce:** peer-reviewed IaC plan, deployment transcript, environment inventory, staging smoke/E2E result, security scanning and pentest report, verified restoration and rollout rollback evidence, estimated and observed spend.

**Gate:** QA + Security + SRE approve staging baseline; no public demo auth, unreviewed IAM wildcards, unencrypted data or unproven restore.

## G5 — Customer pilot

**Tasks:** formally select tenant, users and allowed workflows; authorized representative sample; shadow and read-only mode first; collect human-adjudicated golden labels; compare to human baseline by cohort; train users and support staff; enable only narrowly approved write paths with feature flags; weekly quality/cost/incident reviews; explicit halt conditions.

**Must produce:** `docs/pilot/PILOT_PROTOCOL.md`, `COHORT_AND_CONSENT.md`, `BASELINE_COMPARISON.md`, `PILOT_SCORECARD.md`, `ISSUE_LOG.md`, `PILOT_DECISION.md`.

**Gate:** Product Owner + Security Lead approve results and residual risk. Pilot may be stopped or scope reduced; no assumed promotion.

## G6 — Production readiness review

**Tasks:** negotiate service SLI/SLO and error budget; implement safe dashboards, paging, ownership and runbooks; restore to defined RPO/RTO; prove high availability and capacity; access reviews and data retention; audit export/review; incident drills and postmortem template; release/rollback playbook; support schedule; customer acceptance and change-management approvals.

**Must produce:** `docs/production/PRR_CHECKLIST.md`, `SLO.md`, `RUNBOOKS/`, `DR_REPORT.md`, `SECURITY_APPROVAL.md`, `RELEASE_RECORD.md`.

**Gate:** SRE Lead + Security Lead + Customer Change Owner sign go/no-go with evidence links. Reject missing high-severity security evidence.

## G7 — Production launch and hypercare

**Tasks:** deployment by reviewed GitOps commit and immutable image digest; feature flag off by default; read-only/shadow validation; progressive canary based on predefined SLO/AI risk guardrails; limited write scope; alerts and human escalation active; rollback drill; daily production scorecard and documented defects; closure of high-severity incidents.

**Must produce:** `docs/production/GO_LIVE_RUNBOOK.md`, `CANARY_REPORT.md`, `HYPERCARE_LOG.md`, `PRODUCTION_ACCEPTANCE.md`.

**Gate:** Sustained service performance with customer/SRE signoff and no open release-blocking defect. Deploying containers alone is not acceptance.

## G8 — Operations handover and closeout

**Tasks:** operator training, access transfer without sharing credentials, ownership matrix, paging and escalation test, runbook walkthrough, infrastructure inventory, DR exercise, cost/usage report, support boundaries/SLA, product backlog and customer signoff; archive evidence and interview defense.

**Must produce:** `docs/handover/HANDOVER_CHECKLIST.md`, `OPERATIONS_ACCEPTANCE.md`, `TRAINING_LOG.md`, `FINAL_BUSINESS_REPORT.md`, `LESSONS_LEARNED.md`, `INTERVIEW_DEFENSE.md`.

**Gate:** Named Customer Operations Owner accepts support, documentation, access and recovery responsibility. Sponsor acknowledges closure and remaining backlog.

## Gate decision record — copy for every G0–G8

```text
Gate ID:
Review date (UTC):
Environment / tenant:
Commit SHA:
Image digest:
Test command and CI run URL:
Data source / synthetic-vs-approved:
Security findings and accepted residual risks:
Business results (numerator/denominator):
Evidence links:
Rollback rehearsal:
Decision: GO / NO-GO / CONDITIONAL
Approver names and roles:
Follow-up issue IDs and due dates:
```

**Important:** Approvals are human review records; do not pre-fill or auto-generate a GO.
