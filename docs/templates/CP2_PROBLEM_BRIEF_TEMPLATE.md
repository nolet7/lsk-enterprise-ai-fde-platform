# CP2 — Data-backed customer problem brief (unapproved template)

Status: DRAFT | Customer: fictional Meridian | Owner: Product Owner | FDE preparer: [ ]

## 1. Problem and affected user
[One concise evidence-backed statement; connect to a concrete JTBD.]

## 2. Baseline and evidence
| Metric | Numerator/denominator or statistic | Cleaned source | Date window | Baseline | Target |
|---|---|---|---|---|---|
| Reassigned tickets | count(reassignment_count > 0) / total eligible | TBD | TBD | UNKNOWN | TBD |
| Median resolution hours | medians for reassigned and other tickets | TBD | TBD | UNKNOWN | TBD |
| SLA breached | breaches / eligible by reassignment cohort | TBD | TBD | UNKNOWN | TBD |
| Routing accuracy | correctly assigned / evaluated eligible tickets | TBD | TBD | UNKNOWN | TBD |
| Adoption | active trained users / eligible pilot users | TBD | TBD | UNKNOWN | TBD |

## 3. Ticket-history quality checks (Day 4)
Record raw and clean row counts; duplicated ticket IDs, invalid 9999-hour outliers, blank categories, top category by volume + misroute, first→final resolver pairs, phone channel gap, PII flags, exclusions and rationale. Report *medians* for durations. Attach SQL/notebook and reproducible seed/data provenance. Never invent the missing Northwind source CSV results.

## 4. Data inventory / constraints
| Dataset | Owner | Volume / freshness | Missingness / labels | Sensitivity / residency | Access / retention |
|---|---|---|---|---|---|
| ITSM tickets | TBD | TBD | TBD | TBD | TBD |
| Knowledge base | TBD | TBD | TBD | TBD | TBD |
| Identity / resolver teams | TBD | TBD | TBD | TBD | TBD |

## 5. Qualify AI versus alternative
Problem fit [ ]; measurable value [ ]; deterministic baseline [ ]; usable labels/data [ ]; risk/privacy [ ]; costs [ ]; operational ownership [ ]. Decision with rationale: AI / rules / process / defer.

## 6. Scope agreement
In [ ]; Out [ ] each with reason; channels, regions, users, permitted write classes, measurable exit criteria, consent, constraints, assumptions, escalation and changes.

## 7. CP2 decision
Product Owner [ ]; Sponsor [ ]; Security/Privacy [ ]. No unverified baseline or unstated AI success claim.
