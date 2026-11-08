# LSK Engineering — sequential FDE engagement playbook

**Canonical execution order**: Discover → Define → Design → Build & Integrate → Prove → Hand Over & Expand. This follows the six-step FDE arc in the user-supplied Day 1 workbook. **Engagement models are separate**: POC (can it work?), pilot (value for a bounded real-user cohort?), production (safe daily scaled operations?). Do not use POC/pilot/production as a substitute for discovery and definition.

**Project**: Meridian Financial Services (fictional customer). **Status**: planning document; approval signatures and customer data are simulated until explicitly verified. The functioning deterministic local API is a *technical spike* and can be used for Step 4 when authorized; it is NOT proof that Steps 1–3 are complete. The 16 engineering phases and FDE-001..029 tasks remain as subordinate implementation work packages, not an alternative engagement order.

## Sequential stage map

| Stage | Owner / accountable approver | Entry rule | Ordered activities | Artifact / exit gate |
|---|---|---|---|---|
| S0 Mandate and setup | Engagement Lead / Sponsor | Written CTO request | Confirm problem, engagement model, constraints; kickoff agenda; RACI with exactly one A per decision; meeting cadence; access tracker; 5 early security questions | CP1 engagement charter, RACI and stakeholder map approved (Gate S0) |
| S1 Discover | FDE / Product Owner | S0 accepted | Stakeholder interviews; 45-minute interview arc; gather actual examples and data; F/O/A fact-opinion-assumption log; 5 Whys; jobs-to-be-done; process map; data inventory | Evidence-backed insight statement validated by stakeholders (Gate S1) |
| S2 Define | FDE / Product Owner | S1 accepted | Clean and profile historical tickets; reconcile interview claims; qualify AI versus deterministic/process alternative; baseline business and model KPIs; in/out scope; non-goals, constraints, success metrics, evaluation/holdout rules | CP2 client problem brief and scope agreement (Gate S2) |
| S3 Design | Architect and FDE / Security + Sponsor | S2 accepted | PRD-lite, user stories with acceptance tests, C4 context/container diagrams, 2+ ADRs, threat and responsible AI risk-control matrix, SOW, client responsibilities, change control, three-point estimates, current-price LLM cost model | CP3 approved design package: PRD-lite + architecture + SOW (Gate S3) |
| S4 Build & integrate — POC | FDE / QA | S3 accepted | Use bounded synthetic data and local runtime; implement typed API, reference baseline, test cases and evaluation; reproduce clean-room; demonstrate both initial ingest and replay; run failure/denial cases | Feasibility proven on agreed scenarios; record limits and POC go/no-go (Gate POC) |
| S4 Build & integrate — pilot | FDE / Security + Product Owner | POC go | Approved access and data; real identity/tenant controls; signed integrations; controlled pilot cohort; shadow-mode then guarded writes; training; audit, rollback and independent eval | Pilot ready for measurement; explicit security/customer approval |
| S5 Prove — pilot | FDE / Product Owner + Sponsor | Pilot executed | Compare real-user results against predeclared baselines; track numerator/denominator, slices, confidence where feasible; ROI, cost, risk, RAID/status and executive demo; no synthetic-only success claim | Signed pilot value and safety go/no-go (Gate Pilot) |
| S4 Build & integrate — production hardening | Platform/SRE / Security | Pilot go | Terraform EKS staging/prod, GitOps, SLOs, identity, private data stores, policy-gated actions, tests, monitoring, backup/restore, SBOM/supply chain, secure canary | Formal PRR and change approval (Gate PRR) |
| S5 Prove — production | SRE / Customer Change Owner | PRR go | Progressive rollout, monitored outcomes, failure recovery, performance, error budgets, hypercare, adoption, cost and post-release validation | Customer production acceptance (Gate Production) |
| S6 Hand over & expand | Customer Operations / Sponsor | Production accepted | Runbooks, support roster, access transfer, training, user guides, tested DR and rollback, ongoing evaluation ownership, final results and backlog/expansion proposal | Signed operational handover and engagement closure (Gate Handover) |

**Critical interpretation:** Steps 4 and 5 recur in each deployment model (POC, pilot, production), but discovery/definition/design must be revisited whenever the customer changes scope or assumptions. Do not silently skip previous gates.

## S0 — kickoff and checkpoint CP1

Produce `docs/engagement/CP1_ENGAGEMENT_CHARTER.md` using [CP1 template](templates/CP1_ENGAGEMENT_CHARTER_TEMPLATE.md). Explicitly identify sponsor, product owner, security, privacy, ITSM administrator, resolver teams, end users, audit and the FDE pod. Invite high-impact/high-influence blockers to discovery before development. Create RACI with **one accountable owner per decision**. Establish daily async standup, weekly working session, weekly written status, biweekly sprint demo and steering meeting. File long-lead access requests immediately (SSO/device, read-only API, sanitized sample, approved model vendor, dev environment). Ask: data classification; allowed location/provider/retention; access and least privilege; applicable policy/regulatory requirements; required privacy/security/change approvals. No customer records in Git.

## S1 — discovery interviews, 5 Whys and JTBD

Use the 45-minute interview pattern: open 5m, role/context 5m, last-real-example 15m, pain/workaround 10m, data/constraints 5m, close 5m. Do not pitch an AI solution while discovering. Tag each claim `F` (verifiable fact), `O` (opinion), or `A` (assumption). Ask for the artifact behind important assertions. Complete process map, root-cause chain and job statements in form: `When [situation], I want to [motivation], so I can [outcome]`. Insight statement: `We observed [fact] because [root cause], which costs [impact]. This matters to [stakeholder] because [JTBD].` Use [discovery template](templates/DISCOVERY_INTERVIEW_TEMPLATE.md).

## S2 — qualification and CP2

Day 4's ticket-history method is **clean first, then count**. For a permitted dataset, check duplicate ticket IDs, 9999-hour invalid outliers, blank categories, reassignment frequency, median resolution by reassignment, frequent incorrect first/final group pairs, channel quality, SLA differences and personal-data flags. Preserve raw source, documented cleaning, counts, denominators and reproducible query/notebook. The workbook names a Northwind CSV; **that CSV was not among the supplied attachments**, so do not manufacture those empirical values. Use generated *clearly synthetic* Meridian fixtures if needed.

Record alternative solutions, AI use-case qualification (value, feasibility, data availability, safety/cost), constraints and non-AI fallback. Separate *business KPI* (e.g., reduced reassignment, first response, SLA breaches, adoption) from *model metrics* (routing accuracy, coverage, abstentions, unsafe tool execution). Agree baseline measurement window, target, evaluation method, non-goals and scope with the product owner. Produce [CP2](templates/CP2_PROBLEM_BRIEF_TEMPLATE.md). Do not present proposed baseline percentages as observations.

## S3 — design and CP3

Write PRD-lite with business and user stories, functional/NFR requirements, permissions, data life cycle, testable acceptance, implementation milestones and ownership. C4 context shows people and external systems; container shows responsibilities and data movement; component diagram only where useful. At least two ADRs describe context, alternatives, decision and consequences. Threat/control table must include prompt injection, sensitive disclosure, excess agency, unauthorized retrieval and runaway model cost. Cover fairness slices, transparency, human oversight, privacy, reliability, accountability.

The SOW includes purpose/scope, deliverables and acceptance, milestones and go/no-go, client responsibilities, assumptions, governance, change control and commercial terms. Three-point person-day estimate: `(optimistic + 4*most_likely + pessimistic)/6`, plus explicit contingency. LLM costs: monthly requests × per-request input/output tokens × current model rates, plus evaluations and infrastructure, then cost/transaction. Obtain current provider rates before quoting actual amounts. Produce [CP3](templates/CP3_DESIGN_AND_SOW_TEMPLATE.md).

## Work packages after CP3

**POC:** synthetic/offline data, low-cost local deterministic baseline, optional LLM behind abstraction, no real writes, explicit baseline and failures. **Pilot:** identity, approved cohort, customer workflow, shadow mode before guarded operations, signed action policy, human review and adoption feedback. **Production:** private networking and cloud tenancy, auditable authorization, supply-chain, SLO/DR, tested GitOps deployment and rollback, observed economics. **Handover:** training, operational demonstrations, support responsibilities, final report and expansion plan.

## Reproducibility contract for every stage

Each deliverable records `artifact_id`, `step`, `owner_role`, `reviewer_role`, `status`, `source/evidence`, `commit_sha`, `dataset_version`, `exact_commands`, `expected_output`, `actual_result`, `decision_utc`, and `open_risks`. Tech tasks also record interpreter/container version, transitive lock/image digest, configuration, test suite, seed, rollback and restoration. An approval gate is not a GitHub checkbox; it requires a named reviewer decision. No progression to live data or writes without documented customer/security authorization.

## Source-to-stage mapping (user-supplied workbooks)

- **Day 1:** six-step arc, FDE ownership, POC/pilot/production distinctions and exit criteria.
- **Day 2 / CP1:** kickoff, RACI, cadence, access tracker, security questions and stakeholder mapping.
- **Day 3:** 45-minute non-leading interviews, facts/opinions/assumptions, five Whys, jobs to be done. The completed walkthrough is a **Northwind fictional example**, not Meridian customer evidence.
- **Day 4 / CP2:** ticket-history analysis, data inventory/constraints, AI use-case qualification, success metrics and scope agreement.
- **Day 6 / CP3:** C4, ADRs, risk/control and responsible-AI assessment, SOW, three-point estimation and LLM unit costs.
- **Day 5:** referenced by CP3 but **not provided**, so the PRD-lite content here is a recommended implementation, not a verbatim extraction from Day 5.
- **Days 7–9:** referenced by Day 1 as deeper modules but **not provided**. Pilot/production/handover controls in this document are engineering recommendations supplemented by the existing repo, not purported quotes from those absent workbooks.

## Relation to existing project controls

Keep [EXECUTION_ROADMAP.md](EXECUTION_ROADMAP.md) as technical G0–G8 controls and [TASK_BACKLOG.md](TASK_BACKLOG.md) as task IDs. **Sequence authority is this file.** Previous assumptions of a fixed 16-week full enterprise rollout are superseded; the Day 1 workbook gives indicative POC 2–4 weeks, pilot 6–12 weeks, production phased 3–9 months, subject to actual scope and written gates. A local spike can precede S0 if clearly labeled exploratory, but may not claim engagement acceptance.
