# LSK Enterprise AI Resolution Platform

**Status:** Reproducible, deterministic **local POC only**. This is a safe engineering foundation for a 16-phase FDE delivery simulation, **not** a completed enterprise AI system. No LLM, RAG, CRM/ITSM connector, AWS infrastructure, hardened IAM, or real external writes are implemented yet.

## Why this exists

Fictional customer: Meridian Financial Services. Supplier: LSK Engineering. Goal: demonstrate the CTO mandate-to-production FDE lifecycle while insisting on executable evidence for each stage.

## Requirements

- Python 3.12+ and pip, **or** Docker Engine with Docker Compose v2
- Recommended: Git, VS Code and Windows Git Bash / PowerShell
- No cloud account or API key needed; data is synthetic

## Reproduce locally — Docker (recommended)

```bash
git clone https://github.com/nolet7/lsk-enterprise-ai-fde-platform.git
cd lsk-enterprise-ai-fde-platform
cp .env.example .env
docker compose up --build -d
API_URL=http://127.0.0.1:18000 python scripts/smoke.py
docker compose down
```

For PowerShell replace `cp` with `Copy-Item`. The repository is hosted at the clone URL above.

**Safety:** Docker publishes the API only on `127.0.0.1:18000` (container port `8000`). The `.env` demo key is intentionally public and is NOT a credential for any real environment. NEVER expose the service to the internet or use actual customer data. Compose stores the SQLite DB under disposable `/tmp`; restarting the container can reset demo state. End-to-end persistence is deliberately out of scope for this stage.

## Reproduce locally — Python

```bash
python -m venv .venv
# Git Bash / Linux/macOS: source .venv/bin/activate   (Windows Git Bash: source .venv/Scripts/activate)
# PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
# Git Bash / Linux/macOS
export DEMO_MODE=true DEMO_API_KEY=local-demo-only-change-me
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
# in another shell: python scripts/smoke.py
```

Note: on Windows PowerShell, set environment variables with `$env:DEMO_MODE='true'` and `$env:DEMO_API_KEY='local-demo-only-change-me'` before launching uvicorn.

## Demo API

- GET `/health/live` and `/health/ready`
- POST `/v1/tickets` for deterministic routing + replay-safe event ingestion
- GET `/v1/tickets/{ticket_id}` tenant-scoped lookup
- POST `/v1/actions` create controlled mock-action request
- POST `/v1/actions/{id}/approve` with two-person rule
- POST `/v1/actions/{id}/execute` writes only a simulated local state change
- GET `/v1/audit` tenant-scoped audit log
- `/docs` provides FastAPI-generated API docs

### Demo identity model (INTENTIONALLY NOT PRODUCTION AUTH)

For local testing only, send `X-API-Key`, `X-Tenant`, `X-Actor`, and `X-Role` (`analyst`, `manager`, `approver`, `admin`). These headers are user-controlled and therefore **cannot be trusted** in any deployed product. In production, replace them with validated OIDC access tokens and server-side tenant/role bindings. The app **refuses startup** unless `DEMO_MODE=true`; this is an intentional fail-closed control.

## Sequential FDE engagement — start here

**[Canonical six-step FDE playbook](docs/FDE_SEQUENTIAL_PLAYBOOK.md):** Discover → Define → Design → Build & Integrate → Prove → Hand Over & Expand. Complete [CP1 engagement charter](docs/templates/CP1_ENGAGEMENT_CHARTER_TEMPLATE.md), [discovery evidence](docs/templates/DISCOVERY_INTERVIEW_TEMPLATE.md), [CP2 client problem brief](docs/templates/CP2_PROBLEM_BRIEF_TEMPLATE.md) and [CP3 design/SOW](docs/templates/CP3_DESIGN_AND_SOW_TEMPLATE.md) in sequence. The local app is an engineering spike, not customer acceptance. Existing engineering work-package phases follow the accepted FDE stage, and pilot/production require separate evidence and approvals.

## Architecture and project lifecycle

- **[Execution roadmap and G0–G8 gate evidence](docs/EXECUTION_ROADMAP.md)**
- **[29-task actionable delivery backlog](docs/TASK_BACKLOG.md)**
- **[POC → pilot → production → handover verification runbook](docs/PHASE_VERIFY_RUNBOOK.md)**
- [Mandate and phased delivery plan](docs/DELIVERY_PLAN.md)
- [Architecture decisions and security review](docs/ARCHITECTURE_SECURITY.md)
- [Reproducibility manifest and verification](docs/REPRODUCIBILITY.md)
- [Production backlog and exit criteria](docs/PRODUCTION_GATES.md)
- [Requirements-to-evidence traceability](docs/TRACEABILITY.md)

## What is implemented vs planned

| Capability | Status |
|---|---|
| Local FastAPI service and deterministic routing | Implemented |
| Tenant-scoped local persistence | Implemented for demo only |
| Replay checks and approval-state simulation | Implemented for demo only |
| Local tests and GitHub Actions test/build jobs | Implemented |
| Real OIDC / signed webhook / policy engine | Not implemented |
| External CRM, ITSM, human approval UI | Not implemented |
| AI model, RAG, agent runtime and evaluation | Not implemented |
| Terraform, EKS, Argo CD production environments | Not implemented |
| Observability, HA, DR and regulatory signoff | Not implemented |

## Definition of done

Only a verified phase may be marked complete. The production phase cannot be claimed until security approval, complete evaluation, real operations evidence, customer signoff and recovery testing exist. See `docs/PRODUCTION_GATES.md`.

## License / data

Sample data is fictional. No real customer data or credentials should be committed.
