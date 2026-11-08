> **Execution precedence (2026-11-08):** Follow [FDE_SEQUENTIAL_PLAYBOOK.md](FDE_SEQUENTIAL_PLAYBOOK.md) first: Discover → Define → Design → Build & Integrate → Prove → Hand Over & Expand. CP1, CP2, and CP3 gates precede a customer POC. This document is a technical workstream/backlog reference, NOT permission to implement later phases out of order. The existing local POC is a pre-engagement engineering spike, not a customer-approved POC.

# CTO mandate through customer handover

## Fictional CTO mandate

Meridian Financial Services needs an auditable operational AI workflow system that reduces ticket resolution time, enables trustworthy knowledge search, and executes only explicitly permitted actions. LSK Engineering owns discovery, design, delivery, measured outcomes and operational handover.

## Business case assumptions — not measured achievements

- Baseline mean resolution time: 12 hours; hypothesis: 7 hours.
- Baseline correct routing: 72%; proposed acceptance target: >=95% on blinded, representative, labeled cases.
- Target 99.9% production availability after real SLO negotiation.
- Security invariant: no unauthorized external writes.
- No production promotion based on synthetic accuracy alone.

## Sixteen-phase control plan

| # | Phase | Key artifact | Independent gate |
|---|---|---|---|
| 01 | CTO mandate | charter, scope and RACI | Sponsor authorization |
| 02 | Discovery | interviews and workflows | Product owner requirements signoff |
| 03 | Commercial feasibility | cost, ROI and risk register | Bounded POC funding |
| 04 | Architecture/security | C4, ADR, trust boundaries | Architecture and security review |
| 05 | Engineering foundation | reproducible repo and CI | Clean-room verification |
| 06 | Enterprise integrations | typed schemas and connectors | Contract and resilience tests |
| 07 | Retrieval | indexed authorized corpus | Grounded eval on blind data |
| 08 | Controlled agents | stateful typed tools and policy | Negative security test suite |
| 09 | Identity and customer UI | OIDC and role-aware portal | Cross-tenant E2E tests |
| 10 | POC | signed evaluation report | POC go/no-go |
| 11 | AWS/GitOps | Terraform, EKS, Helm and Argo CD | Staging rollout / rollback |
| 12 | Quality and AI safety | load, red team, evals | Security/QA acceptance |
| 13 | Customer pilot | real pilot scorecard | Business and risk approval |
| 14 | Operational readiness | SLO, DR and runbooks | Formal PRR approval |
| 15 | Production hypercare | canary evidence and incidents | Stable service acceptance |
| 16 | Handover | training and operator signoff | Customer closes engagement |

## Delivery ownership

FDE lead drives the customer workstream, engineering implementation and evidence. Customer CTO sponsors; operations owns the service after handover; customer security accepts residual risk; product owner approves workflow requirements; SRE controls release and reliability. No self-approval by the implementer.

## Pilot design

- Use synthetic samples for POC; independently labeled representative non-sensitive or authorized samples for pilot.
- Shadow mode first; human review for low-risk suggestions.
- Introduce writes only after permissions, audit, idempotency and a rollback strategy are proven.
- Compare against a documented human/deterministic baseline and segment by workflow and failure mode.
- Record denominator, confidence intervals where applicable, user adoption, manual review burden, costs, errors and operator interventions.

## Release and change management

Every environment promotion references immutable artifact digest, commit SHA, test report, owner approvals and rollback procedure. Design docs and successful code are not a substitute for measured production evidence.
