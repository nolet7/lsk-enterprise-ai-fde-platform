# CP3 — PRD-lite, solution design and SOW (unapproved template)

**Dependencies:** CP1 and CP2 accepted; do not treat local code as implied acceptance. **Status:** DRAFT.

## 1. PRD-lite
Problem statement [ ]; users and JTBD [ ]; scenarios [ ]; stories [ ]; functional requirements [ ]; NFRs [ ]; permissions [ ]; KPIs with denominator [ ]; out-of-scope [ ]; error handling [ ]; accessibility [ ]; test/eval acceptance and owner [ ].

## 2. C4 model
- Context: analyst, service desk lead, ITSM, IdP, compliance, external model provider.
- Container: portal, API, routing, policy/approval, retrieval, PostgreSQL, logging.
- Relationships: source, destination, protocol, trust boundary, sensitive data and retention.
- Reference diagrams under `docs/architecture/`; do not draw unimplemented boxes as deployed facts.

## 3. ADRs
ADR-001: routing baseline rules versus LLM; context/options/decision/consequences/status [ ].
ADR-002: tenant-isolation and OIDC server-bound claims; context/options/decision/consequences/status [ ].

## 4. Threat and responsible AI
| Risk | Required control | Owner | Test evidence |
|---|---|---|---|
| Prompt injection / bad route | output allowlist + independent policy gate | AI/Security | adversarial eval |
| Confidential data in prompt/log | redaction/minimization and retention | Security | redaction tests |
| Excess agency | read-only default + human approvals | Product/Security | denied write E2E |
| Unauthorized retrieval | identity-bound ACL retrieval | Platform/Security | cross-tenant tests |
| Runaway spend | quotas, timeouts, cost alerts | Platform/Finance | burst test |

Fairness slices [ ]; user transparency [ ]; human oversight and stop [ ]; privacy [ ]; regression monitoring [ ]; accountability [ ].

## 5. SOW outline
1. Purpose and scope [ ].
2. Deliverables and objective acceptance criteria [ ].
3. Milestones and stage go/no-go [ ].
4. Client access, people, approvals and dates [ ].
5. Assumptions, exclusions and dependencies [ ].
6. FDE pod and governance [ ].
7. Change request approval and cost/schedule impact [ ].
8. Commercial model as agreed [ ].

## 6. Three-point engineering estimate
For each workstream, person-days `E=(O+4M+P)/6` (optimistic / most likely / pessimistic); total, contingency, capacity assumptions, blocked access lead time and dependencies. Record actual estimates only after scoping.

## 7. Model operating cost
Monthly requests [ ] × (input tokens/request [ ] × current input $/1M [ ] + output tokens/request [ ] × current output $/1M [ ])/1,000,000. Plus embedding, eval, storage, networking, observability and environment costs. Compute total and per transaction. Vendor price citation and date REQUIRED.

## CP3 review
Solution architect [ ]; Security [ ]; Product Owner [ ]; Sponsor [ ]; review date [ ]; signed SOW [ ]. No production release permission implied.
