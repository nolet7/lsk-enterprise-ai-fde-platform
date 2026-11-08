# Reproducibility contract

## Local reproducibility

A clean environment must be able to clone, install, test, run and smoke-test without external keys. Python and Docker routes are in README. Run `python -m pytest -q`; a passing suite must include unauthorized access, tenant boundaries, replay conflict, abstention, separation of duties and duplicate execution denial.

## Version contract

- Python target: 3.12 (CI and container); Python 3.12+ for developer test environment.
- Dockerfile base: `python:3.12.8-slim` (version pinned, digest not yet pinned; security release must pin digest).
- Python direct dependencies: exactly pinned in requirements files; the fully transitive dependency graph is **not** locked yet. Before a release generate a platform-appropriate hashed lock file with pip-tools or uv and require frozen installs.
- Dependencies are intentionally small; local SQLite and deterministic routing eliminate network/model requirements.

## Validation checklist

1. `git clone <repository-url>`, create `.env` from `.env.example`.
2. `python -m pip install -r requirements-dev.txt`.
3. `python -m pytest -q` (report environment and pass count).
4. `docker compose config` and `docker compose up --build -d`.
5. `python scripts/smoke.py` (expect PASS smoke).
6. Open `http://127.0.0.1:8000/docs` for the OpenAPI document.
7. `docker compose down` to clean up.
8. Confirm `git status --short` is empty; .env and generated DB are ignored.

## Test data and state

Input is generated directly in tests or supplied as fake samples. Data path `DATABASE_PATH` is injectable; tests create a fresh isolated SQLite DB for each test. The Docker instance intentionally uses ephemeral `/tmp/demo.db`. Neither durability nor HA is claimed. There are no live third-party credentials or dependencies.

## Reproducibility evidence to record after each change

Commit SHA; dependency lock digest; Python/platform version; container image digest; exact commands; test result; smoke output; known limitations; external services versions when introduced; recovery procedure.

## Failure protocol

If a command fails, collect the exact command, stderr, platform, interpreter version and `git rev-parse HEAD`, then open an issue. Do not claim a phase complete after an untested fix.
