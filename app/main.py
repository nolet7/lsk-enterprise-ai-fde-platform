"""LSK FDE proof-of-concept. NOT an internet-facing or regulated-production service."""
import hmac
import os
import sqlite3
import uuid
from contextlib import contextmanager, asynccontextmanager
from datetime import datetime, timezone
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field




def now():
    return datetime.now(timezone.utc).isoformat()


def config():
    if os.getenv("DEMO_MODE", "false").lower() != "true":
        raise RuntimeError("Refusing to start: DEMO_MODE is not true. Production auth is not implemented.")
    key = os.getenv("DEMO_API_KEY", "")
    if not key or len(key) < 16:
        raise RuntimeError("DEMO_API_KEY must be at least 16 characters")
    return key


def initialize():
    config()
    with db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS tickets (
            tenant TEXT NOT NULL, id TEXT NOT NULL, event_id TEXT NOT NULL,
            description TEXT NOT NULL, route TEXT NOT NULL, rationale TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (tenant,id), UNIQUE(tenant,event_id)
        );
        CREATE TABLE IF NOT EXISTS actions (
            tenant TEXT NOT NULL, id TEXT NOT NULL, ticket_id TEXT NOT NULL,
            kind TEXT NOT NULL, state TEXT NOT NULL, requested_by TEXT NOT NULL,
            approved_by TEXT, created_at TEXT NOT NULL,
            PRIMARY KEY (tenant,id)
        );
        CREATE TABLE IF NOT EXISTS audit (
            id TEXT PRIMARY KEY, tenant TEXT NOT NULL, subject TEXT NOT NULL,
            event TEXT NOT NULL, resource TEXT NOT NULL, at TEXT NOT NULL
        );
        """)


@asynccontextmanager
async def lifespan(_app):
    initialize()
    yield


app = FastAPI(title="LSK Enterprise AI Resolution - deterministic reference POC", version="0.1.0", lifespan=lifespan)


@contextmanager
def db():
    path = os.getenv("DATABASE_PATH", "./demo.db")
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


class Identity(BaseModel):
    tenant: str
    actor: str
    role: Literal["analyst", "manager", "approver", "admin"]


def identity(x_api_key: str = Header(default=""), x_tenant: str = Header(default=""),
             x_actor: str = Header(default=""), x_role: str = Header(default="")) -> Identity:
    expected = config()
    if not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(401, "Invalid demo API key")
    try:
        return Identity(tenant=x_tenant, actor=x_actor, role=x_role)
    except Exception:
        raise HTTPException(401, "Demo identity headers missing or invalid")


def authorize(user: Identity, allowed: set):
    if user.role not in allowed or not user.tenant.strip() or not user.actor.strip():
        raise HTTPException(403, "Forbidden")


def audit(conn, user: Identity, event: str, resource: str):
    conn.execute("INSERT INTO audit VALUES (?,?,?,?,?,?)", (str(uuid.uuid4()), user.tenant, user.actor, event, resource, now()))


def route(description: str) -> tuple[str, str]:
    """Deliberate deterministic baseline, not an LLM or trained classifier."""
    t = description.lower()
    if any(k in t for k in ["login", "sign in", "access", "password"]):
        return "identity", "Matched access/identity keywords; analyst must review"
    if any(k in t for k in ["billing", "invoice", "payment"]):
        return "billing", "Matched billing keywords; analyst must review"
    if any(k in t for k in ["latency", "outage", "timeout", "slow"]):
        return "platform", "Matched platform keywords; analyst must review"
    return "manual-review", "Insufficient deterministic evidence; no auto-route"


class TicketIn(BaseModel):
    event_id: str = Field(min_length=1, max_length=128)
    ticket_id: str = Field(min_length=1, max_length=128)
    description: str = Field(min_length=5, max_length=4000)


class ActionIn(BaseModel):
    ticket_id: str = Field(min_length=1, max_length=128)
    kind: Literal["add-internal-note"]


@app.get("/health/live")
def live():
    return {"status": "live"}


@app.get("/health/ready")
def ready():
    config()
    with db() as conn:
        conn.execute("SELECT 1").fetchone()
    return {"status": "ready"}


@app.post("/v1/tickets", status_code=status.HTTP_201_CREATED)
def ingest(payload: TicketIn, user: Identity = Depends(identity)):
    authorize(user, {"analyst", "admin"})
    assigned, why = route(payload.description)
    with db() as conn:
        old = conn.execute("SELECT * FROM tickets WHERE tenant=? AND event_id=?", (user.tenant, payload.event_id)).fetchone()
        if old:
            if old["id"] != payload.ticket_id or old["description"] != payload.description:
                raise HTTPException(409, "Idempotency key reused with a different payload")
            return {"ticket_id": old["id"], "route": old["route"], "idempotent_replay": True}
        if conn.execute("SELECT 1 FROM tickets WHERE tenant=? AND id=?", (user.tenant, payload.ticket_id)).fetchone():
            raise HTTPException(409, "Ticket id already exists")
        conn.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?,?)",
                     (user.tenant, payload.ticket_id, payload.event_id, payload.description, assigned, why, now()))
        audit(conn, user, "ticket.created", payload.ticket_id)
    return {"ticket_id": payload.ticket_id, "route": assigned, "rationale": why, "idempotent_replay": False}


@app.get("/v1/tickets/{ticket_id}")
def ticket(ticket_id: str, user: Identity = Depends(identity)):
    authorize(user, {"analyst", "manager", "approver", "admin"})
    with db() as conn:
        row = conn.execute("SELECT id, description, route, rationale, created_at FROM tickets WHERE tenant=? AND id=?",
                           (user.tenant, ticket_id)).fetchone()
    if not row:
        raise HTTPException(404, "Not found")
    return dict(row)


@app.post("/v1/actions", status_code=201)
def request_action(payload: ActionIn, user: Identity = Depends(identity)):
    authorize(user, {"analyst", "admin"})
    with db() as conn:
        if not conn.execute("SELECT 1 FROM tickets WHERE tenant=? AND id=?", (user.tenant, payload.ticket_id)).fetchone():
            raise HTTPException(404, "Ticket not found")
        action_id = str(uuid.uuid4())
        conn.execute("INSERT INTO actions VALUES (?,?,?,?,?,?,?,?)", (user.tenant, action_id, payload.ticket_id,
                     payload.kind, "pending", user.actor, None, now()))
        audit(conn, user, "action.requested", action_id)
    return {"action_id": action_id, "state": "pending"}


@app.post("/v1/actions/{action_id}/approve")
def approve(action_id: str, user: Identity = Depends(identity)):
    authorize(user, {"approver", "admin"})
    with db() as conn:
        a = conn.execute("SELECT * FROM actions WHERE tenant=? AND id=?", (user.tenant, action_id)).fetchone()
        if not a:
            raise HTTPException(404, "Action not found")
        if a["requested_by"] == user.actor:
            raise HTTPException(403, "Two-person approval required")
        if a["state"] != "pending":
            raise HTTPException(409, "Action is no longer pending")
        conn.execute("UPDATE actions SET state='approved', approved_by=? WHERE tenant=? AND id=?",
                     (user.actor, user.tenant, action_id))
        audit(conn, user, "action.approved", action_id)
    return {"action_id": action_id, "state": "approved"}


@app.post("/v1/actions/{action_id}/execute")
def execute(action_id: str, user: Identity = Depends(identity)):
    authorize(user, {"admin"})
    with db() as conn:
        a = conn.execute("SELECT * FROM actions WHERE tenant=? AND id=?", (user.tenant, action_id)).fetchone()
        if not a:
            raise HTTPException(404, "Action not found")
        if a["state"] != "approved":
            raise HTTPException(409, "Action must be approved")
        # Controlled mock ONLY. No remote credentials or external write integration exists.
        conn.execute("UPDATE actions SET state='simulated-executed' WHERE tenant=? AND id=?", (user.tenant, action_id))
        audit(conn, user, "action.simulated", action_id)
    return {"action_id": action_id, "state": "simulated-executed", "external_write": False}


@app.get("/v1/audit")
def audit_log(user: Identity = Depends(identity)):
    authorize(user, {"manager", "admin"})
    with db() as conn:
        records = conn.execute("SELECT subject, event, resource, at FROM audit WHERE tenant=? ORDER BY at, id",
                               (user.tenant,)).fetchall()
    return [dict(r) for r in records]
