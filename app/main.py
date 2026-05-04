from fastapi import FastAPI

from app.router import router

# FastAPI() crea la aplicación; title y version aparecen en /docs
app = FastAPI(title="OCI Integrator API", version="0.1.0")

# Registra todas las rutas definidas en router.py
app.include_router(router)
