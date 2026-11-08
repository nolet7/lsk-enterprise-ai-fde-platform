# Reproduction and promotion runbook

This runbook complements [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and documents verified local behavior separately from proposed enterprise commands.

## Current local POC (verified on operator Windows Docker environment)

Prerequisites: Git, Docker Desktop with Compose v2 and Python 3.12+. Run from repository root.

```bash
git status --short
git rev-parse HEAD
cp .env.example .env
docker compose config
docker compose up --build -d
docker compose ps
API_URL=http://127.0.0.1:18000 python scripts/smoke.py
python -m pip install -r requirements-dev.txt
python -m pytest -q
docker compose down
```

Expected host binding: `127.0.0.1:18000->8000/tcp`. Internal container health remains `127.0.0.1:8000/health/live`. `/docs` is accessible at `http://127.0.0.1:18000/docs` while running.

**Current smoke limitation:** `scripts/smoke.py` always sends `smoke-e1`. A result of `idempotent_replay=True` means an earlier request was replayed, not that the new-insert path was checked in that invocation. FDE-006 must add a unique-id test with an explicit duplicate request and conflicting payload rejection. Do not delete a running instance's state just to force a screenshot.

**Risk:** `.env.example` contains a public demo token. Loopback-only local testing. No reverse proxy/tunnel or production data. SQLite state is ephemeral.

## Evidence capture template

Create an evidence manifest for each phase, without secrets or customer PII:

```yaml
task_id: FDE-###
phase: POC|STAGING|PILOT|PROD|HANDOVER
status: NOT_VERIFIED
commit_sha: ""
image_digest: ""
dataset_version: ""
model_version: ""
environment: ""
pr_url: ""
ci_run_url: ""
test_commands: []
test_results: []
failed_tests: []
rollback_or_reset: ""
reviewer: ""
approval_date_utc: ""
open_risks: []
```

## Required promotion order

`local POC -> staging -> shadow pilot -> approved pilot writes -> PRR -> canary production -> full production -> handover`.

To progress: all blocking task dependencies must be VERIFIED, test artifacts must match the exact promoted immutable digest, changes must be peer reviewed, security and product reviewers must approve the same risk scope, and rollback must be demonstrated in the intended environment.

Stop immediately if cross-tenant access, unapproved writes, audit gaps, unresolved critical security vulnerabilities, unexplained AI quality regression, or breach of agreed error budgets occurs. Freeze writes using the kill switch and follow incident runbooks once implemented. These safeguards are **requirements**, not functioning guarantees of today's demo.

## Pilot protocol checklist

- Authorized representative cases and human-adjudicated labels; never claim success on only synthetic scores.
- Baseline versus treatment comparison, with selection criteria, denominator and uncertainty disclosed.
- Shadow operation first; approval of model/tool scope before writes.
- Guardrails: hallucination/abstention rates, policy denies, manual override rates, latency, incident count and cost.
- Rollback exercise and operator training evidence.
- Signed decision that identifies scope allowed into production readiness.

## Production launch checklist

- Immutable image digest and IaC plan recorded, independent security scan and approvals filed.
- Negotiated SLO, restore tests, retention and access reviews complete.
- On-call contacts, pager tests, customer communications and escalation operational.
- Feature-flag canary sequence, monitoring window and abort criteria approved.
- Rollback records and evidence of service recovery.
- Signed production acceptance, not assumed from a green deploy.

## Handover checklist

- Customer owns operational runbooks, admin access and billing/monitoring responsibilities.
- Access transfer completed via appropriate identity controls, not shared passwords.
- Operator demonstrates a fresh-clone or clean-environment deployment, simulated incident, rollback and restore.
- Risks, dependencies, escalation, vendor contact paths and backlog are understood.
- Business outcome report includes actual pilot/production measures, sources and limitations.
- Final dated signoff by Sponsor and Customer Operations Owner.
