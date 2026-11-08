# CP1 — Engagement charter (unapproved template)

**Customer:** Meridian Financial Services (fictional) | **Vendor:** LSK Engineering | **Status:** DRAFT — no customer signoff

## CTO mandate in sponsor's words
[Record interview-confirmed request; current concept of faster audited ticket resolution is a hypothesis.]

## Business goal and current baseline
| Metric | Measurement source | Window | Baseline | Proposed target | Owner |
|---|---|---|---|---|---|
| First response time | TBD | TBD | UNKNOWN | TBD | Product Owner |
| Reassignment rate | TBD | TBD | UNKNOWN | TBD | Product Owner |
| Adoption | TBD | TBD | UNKNOWN | TBD | Product Owner |

## Scope
- In scope: [exact ticket categories, region, user cohort and systems]
- Out of scope: [sensitive flows, production auto-write, customer PII until approved]
- POC/pilot/production stage requested: [choose and justify]
- Budget/engagement term and stop conditions: [fill]

## Stakeholder map
| Role | Name/fictional placeholder | Decision rights | Influence/interest | Interview date |
|---|---|---|---|---|
| Sponsor/CTO | TBD | Funding and priority | High/high | TBD |
| Product owner | TBD | Workflow and KPI acceptance | High/high | TBD |
| CISO | TBD | Security risk | High/high | TBD |
| Privacy/DPO | TBD | Data approval | High/high | TBD |
| ITSM admin | TBD | API access | High/high | TBD |
| Resolver leads | TBD | Route validation | High/high | TBD |
| Analyst champions | TBD | Usability | Medium/high | TBD |
| Audit | TBD | Control evidence | Medium/high | TBD |

## Decision RACI (exactly one A per row)
| Decision | R | A | C | I |
|---|---|---|---|---|
| Success metrics | FDE | Product Owner | Sponsor, analysts | Security |
| Data extract approval | ITSM admin | Customer data owner | Privacy/Security | FDE |
| Security acceptance | Security lead | Customer CISO | Platform/FDE | Sponsor |
| POC go/no-go | FDE | Sponsor | Product Owner, Security | Team |
| Pilot user training | FDE | Product Owner | Analyst champion | Sponsor |
| Production change | SRE | Customer change owner | CISO, Product Owner | Sponsor |

## Meeting cadence
- Daily 5m async blocker update; weekly customer working meeting; weekly written status; fortnightly demo; steering decisions at agreed intervals.

## Access tracker
| Requested item | Client owner | Requested | Required by | Approved? | Safe workaround |
|---|---|---|---|---|---|
| SSO and devices | TBD | TBD | TBD | NO | Local fake identities |
| Sanitized history sample | TBD | TBD | TBD | NO | Synthetic fixtures |
| ITSM read-only API | TBD | TBD | TBD | NO | Mock contract |
| Approved model endpoint | TBD | TBD | TBD | NO | Deterministic baseline |
| Sandbox environment | TBD | TBD | TBD | NO | Local Docker |

## Five security questions
1. Data classification and records in scope? [unknown]
2. Residency, vendor approval, training/retention conditions? [unknown]
3. Identities, access and audit requirements? [unknown]
4. Applicable law, company rules, AI controls? [unknown — legal confirmation required]
5. Privacy, vendor, AI and change review boards/dates? [unknown]

## Risks, escalation and first 10 working days
[RAID items, decisions, owner, due date; no live-data work until approved.]

## CP1 Gate
Sponsor [ ], Product Owner [ ], Security [ ]; reviewer names, UTC dates, comments and evidence URLs blank until genuinely approved.
