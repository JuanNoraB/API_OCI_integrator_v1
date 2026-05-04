from pydantic import BaseModel


# ── Request bodies (lo que el cliente ENVÍA) ──────────────────────────────────

class ItemIn(BaseModel):
    name: str
    value: float


# ── Response bodies (lo que la API DEVUELVE) ──────────────────────────────────

class ItemOut(BaseModel):
    id: int
    name: str
    value: float
    message: str


class JobCreated(BaseModel):
    job_id: str
    status: str


class JobStatus(BaseModel):
    job_id: str
    status: str  # "pending" | "done"
