def test_auth_enforced(client, headers):
    assert client.get("/v1/tickets/T1").status_code == 401
    assert client.get("/health/ready").status_code == 200


def test_tenant_isolation_and_idempotency(client, headers):
    payload = {"event_id": "E1", "ticket_id": "T1", "description": "Cannot login to portal"}
    first = client.post("/v1/tickets", headers=headers(), json=payload)
    assert first.status_code == 201 and first.json()["route"] == "identity"
    assert client.post("/v1/tickets", headers=headers(), json=payload).json()["idempotent_replay"]
    modified = {**payload, "description": "Billing system is slow"}
    assert client.post("/v1/tickets", headers=headers(), json=modified).status_code == 409
    assert client.get("/v1/tickets/T1", headers=headers(tenant="other")).status_code == 404
    assert client.get("/v1/tickets/T1", headers=headers()).status_code == 200


def test_approval_and_denials(client, headers):
    client.post("/v1/tickets", headers=headers(), json={"event_id": "E1", "ticket_id": "T1", "description": "billing issue happened"})
    action = client.post("/v1/actions", headers=headers(), json={"ticket_id":"T1", "kind":"add-internal-note"})
    assert action.status_code == 201
    aid = action.json()["action_id"]
    assert client.post(f"/v1/actions/{aid}/execute", headers=headers(role="admin")).status_code == 409
    assert client.post(f"/v1/actions/{aid}/approve", headers=headers(role="approver")).status_code == 403
    assert client.post(f"/v1/actions/{aid}/approve", headers=headers(actor="bob",role="approver")).status_code == 200
    assert client.post(f"/v1/actions/{aid}/execute", headers=headers(actor="carol",role="admin")).json()["external_write"] is False
    assert client.post(f"/v1/actions/{aid}/execute", headers=headers(actor="carol",role="admin")).status_code == 409
    assert len(client.get("/v1/audit", headers=headers(role="manager")).json()) == 4
    assert client.get("/v1/audit", headers=headers(tenant="other",role="manager")).json() == []


def test_abstains(client, headers):
    resp = client.post("/v1/tickets", headers=headers(), json={"event_id":"E2", "ticket_id":"T2", "description":"Question about holiday schedules"})
    assert resp.json()["route"] == "manual-review"


def test_role_authorization(client, headers):
    p = {"event_id":"E1", "ticket_id":"T1", "description":"Identity login issue"}
    assert client.post("/v1/tickets", headers=headers(role="manager"), json=p).status_code == 403
    assert client.get("/v1/audit",headers=headers()).status_code == 403
