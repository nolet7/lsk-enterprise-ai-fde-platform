.PHONY: setup test run up down smoke check
setup:
	python -m pip install -r requirements-dev.txt
test:
	python -m pytest -q
run:
	DEMO_MODE=true DEMO_API_KEY=local-demo-only-change-me python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
up:
	docker compose up --build -d
down:
	docker compose down
smoke:
	python scripts/smoke.py
check: test
