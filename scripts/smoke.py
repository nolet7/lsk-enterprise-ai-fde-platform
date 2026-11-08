"""Execute against localhost:8000 started by docker compose or uvicorn."""
import json
import os
import urllib.request

BASE = os.getenv("API_URL", "http://127.0.0.1:8000")
HEADERS = {"X-API-Key":os.getenv("DEMO_API_KEY", "local-demo-only-change-me"),
           "X-Tenant":"meridian-demo", "X-Actor":"smoke-user", "X-Role":"analyst", "Content-Type":"application/json"}
req = urllib.request.Request(BASE + "/v1/tickets", data=json.dumps({"event_id":"smoke-e1","ticket_id":"smoke-t1","description":"Cannot login to billing portal"}).encode(), headers=HEADERS, method="POST")
with urllib.request.urlopen(req, timeout=10) as resp:
    result=json.load(resp)
assert result["route"] == "identity", result
print("PASS smoke", result)
