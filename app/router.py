import asyncio
import time
import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.models import ItemIn, ItemOut, JobCreated, JobStatus

# APIRouter agrupa endpoints; main.py lo registra en la app principal
router = APIRouter()

# Almacén en memoria de jobs: { job_id: "pending" | "done" }
# En producción esto sería una tabla en BD
jobs: dict[str, str] = {}


# ── 1. Petición simple ────────────────────────────────────────────────────────
# `def` normal: no hay ningún await adentro, no tiene sentido usar async.

@router.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {"status": "ok", "message": "pong"}


# ── 2. async / await  →  simula espera de I/O externo (BD, API, disco) ─────────
# `async def` tiene sentido SOLO porque adentro hay un `await`.
# `await asyncio.sleep(0.5)` simula esperar respuesta de una BD lenta.
# Mientras espera, el event loop atiende OTRAS peticiones → concurrencia real.

@router.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemIn):
    await asyncio.sleep(5)            # ← simula INSERT lento en BD
    return ItemOut(
        id=1,
        name=item.name,
        value=item.value,
        message="Item guardado correctamente",
    )


# ── 3. Background job  →  proceso largo FUERA del ciclo HTTP ──────────────────
# El endpoint responde 202 INMEDIATAMENTE con el job_id.
# El trabajo pesado corre en segundo plano y actualiza `jobs[job_id]`.
# El cliente puede consultar GET /jobs/{job_id} para ver si terminó.

def _long_process(job_id: str) -> None:
    """Simula trabajo pesado/bloqueante (CPU, archivo grande, etc.).
    Al ser `def` normal (no async), FastAPI la corre en un thread pool:
    el event loop queda libre para seguir atendiendo otras peticiones.
    """
    time.sleep(15)                       # ← bloquea el thread, NO el event loop
    jobs[job_id] = "done"


@router.post("/jobs", response_model=JobCreated, status_code=status.HTTP_202_ACCEPTED)
def create_job(background_tasks: BackgroundTasks):  # no hay await adentro → def normal
    job_id = str(uuid.uuid4())          # ID único para este job
    jobs[job_id] = "pending"
    background_tasks.add_task(_long_process, job_id)   # no bloquea, responde ya
    return JobCreated(job_id=job_id, status="pending")


@router.get("/jobs/{job_id}", response_model=JobStatus, status_code=status.HTTP_200_OK)
def get_job(job_id: str):  # `def` normal: solo consulta un dict, cero I/O
    if job_id not in jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job '{job_id}' no encontrado",
        )
    return JobStatus(job_id=job_id, status=jobs[job_id])
